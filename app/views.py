import os
import cv2
import dlib
import numpy as np
from app import app
from PIL import Image
from flask import request, render_template

app.config['GENERATED_FILE'] = 'app/static/generated'
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('app/static/predictors/shape_predictor_68_face_landmarks.dat')


def FindFeaturePoints(img):
    faces = detector(img)
    for face in faces:
        landmarks = predictor(img, face)
        points = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            points.append((x, y))

    return np.array(points, dtype=np.int32)


def FindDelaunayTriangles(points):
    convexhull = cv2.convexHull(points)
    bounding_rectangle = cv2.boundingRect(convexhull)

    triangles = cv2.Subdiv2D(bounding_rectangle)
    triangles.insert(points.tolist())
    triangles = triangles.getTriangleList()
    return np.array(triangles, dtype=np.int32)


def triangle_indices_to_list(triangle_indices, points):
    triangles = []
    for indices in triangle_indices:
        point_1 = points[indices[0]]
        point_2 = points[indices[1]]
        point_3 = points[indices[2]]

        triangles.append(np.array([point_1, point_2, point_3], dtype=np.int32))

    return np.array(triangles)


def RelativeTriangle(triangle):
    point_1 = triangle[0]
    point_2 = triangle[1]
    point_3 = triangle[2]

    x, y, _, _ = cv2.boundingRect(triangle)

    points = np.array([[point_1[0] - x, point_1[1] - y],
                       [point_2[0] - x, point_2[1] - y],
                       [point_3[0] - x, point_3[1] - y]])

    return points


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # Get Uploaded Images
        src_img = Image.open(request.files['src_img_upload'])
        dest_img = Image.open(request.files['dest_img_upload'])

        src_img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'src_image.jpg'))
        dest_img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'dest_image.jpg'))

        src_img = np.array(src_img)
        dest_img = np.array(dest_img)

        # Converting to GrayScale
        src_gray_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
        dest_gray_img = cv2.cvtColor(dest_img, cv2.COLOR_RGB2GRAY)

        # Calculating Feature points of Faces
        src_points = FindFeaturePoints(src_gray_img)
        dest_points = FindFeaturePoints(dest_gray_img)

        # Calculating Delaunay Triangles of Faces
        src_triangles = FindDelaunayTriangles(src_points)

        # Making list of triangle indices
        triangles_indices = []
        for triangle in src_triangles:
            point_1 = np.array((triangle[0], triangle[1]))
            point_2 = np.array((triangle[2], triangle[3]))
            point_3 = np.array((triangle[4], triangle[5]))

            index_1 = np.argwhere((src_points == np.array(point_1)).all(axis=1))[0][0]
            index_2 = np.argwhere((src_points == np.array(point_2)).all(axis=1))[0][0]
            index_3 = np.argwhere((src_points == np.array(point_3)).all(axis=1))[0][0]

            triangles_indices.append([index_1, index_2, index_3])

        # Making list of triangles of shape
        src_triangles = triangle_indices_to_list(triangles_indices, src_points)
        dest_triangles = triangle_indices_to_list(triangles_indices, dest_points)

        # Generate New Face
        new_face_img = np.zeros_like(dest_img)

        for src_triangle, dest_triangle in zip(src_triangles, dest_triangles):
            rel_src_triangle = RelativeTriangle(src_triangle)
            rel_dest_triangle = RelativeTriangle(dest_triangle)

            # Get Triangle from source image
            x, y, w, h = cv2.boundingRect(src_triangle)
            cropped_src_triangle = src_img[y: y + h, x: x + w]

            # Make mask for destination image
            x, y, w, h = cv2.boundingRect(dest_triangle)
            cropped_dest_mask = np.zeros((h, w), dtype=np.uint8)
            cv2.fillConvexPoly(cropped_dest_mask, rel_dest_triangle, 255)
            cv2.line(cropped_dest_mask, rel_dest_triangle[0], rel_dest_triangle[1], 255, 1)
            cv2.line(cropped_dest_mask, rel_dest_triangle[0], rel_dest_triangle[2], 255, 1)
            cv2.line(cropped_dest_mask, rel_dest_triangle[1], rel_dest_triangle[2], 255, 1)

            # Affine Transform cropped source triangle to destination triangle
            M = cv2.getAffineTransform(np.float32(rel_src_triangle), np.float32(rel_dest_triangle))
            warped_triangle = cv2.warpAffine(cropped_src_triangle, M, (w, h))
            warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_dest_mask)

            # Construct destination face
            cropped_new_face = new_face_img[y: y + h, x: x + w]
            cropped_new_face_gray = cv2.cvtColor(cropped_new_face, cv2.COLOR_RGB2GRAY)
            _, opposite_mask = cv2.threshold(cropped_new_face_gray, 1, 255, cv2.THRESH_BINARY_INV)  # To take care of triangle borders

            warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=opposite_mask)

            cropped_new_face = cv2.add(cropped_new_face, warped_triangle)
            new_face_img[y: y + h, x: x + w] = cropped_new_face

            # Swap New face with face in destination image
            dest_convexhull = cv2.convexHull(dest_points)
            dest_face_mask = np.zeros_like(dest_gray_img, dtype=np.uint8)
            dest_face_mask = cv2.fillConvexPoly(dest_face_mask, dest_convexhull, 255)
            dest_opposite_face_mask = cv2.bitwise_not(dest_face_mask)

            swap_img = cv2.bitwise_and(dest_img, dest_img, mask=dest_opposite_face_mask)
            swap_img = cv2.add(swap_img, new_face_img)

            # Correct colours with seamlessclone
            (x, y, w, h) = cv2.boundingRect(dest_convexhull)
            center = ((x + x + w) // 2, (y + y + h) // 2)
            swap_img = cv2.seamlessClone(swap_img, dest_img, dest_face_mask, center, cv2.NORMAL_CLONE)

            swap_img = Image.fromarray(swap_img)
            filepath = os.path.join(app.config['GENERATED_FILE'], 'image.jpg')
            swap_img.save(filepath)

        return render_template('index.html', src_img='static/uploads/src_image.jpg', dest_img='static/uploads/dest_image.jpg', result='static/generated/image.jpg')
