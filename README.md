<a name="readme-top"></a>

<div align="center">

# __Face Swapping__

### Built Using
  
[![Python][python-shield]][python-url]
[![html-css-js][html-css-js-shield]][html-css-js-url]
[![Flask][flask-shield]][flask-url]
[![OpenCV][opencv-shield]][opencv-url]
[![Dlib][dlib-shield]][dlib-url]

Visit the <a href="">Web Application</a> deployed on render

</div>

## __About__
<p align="justify">
This Web Application swaps faces in two images using <a href="https://en.wikipedia.org/wiki/Delaunay_triangulation">Delaunay Triangulation</a> and <a href="https://en.wikipedia.org/wiki/Affine_transformation">Affine Transformation</a>.

Sample Images:

- https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx8Pu1tW1uCiZPfj9K1EL6uHxbg3bOKO9XkA&usqp=CAU

- https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYX1dyl9INRo5cbvDeTILRcZVzfcMsCsE0kg&usqp=CAU

Pretrained Dlib Predictor: https://github.com/tzutalin/dlib-android/raw/master/data/shape_predictor_68_face_landmarks.dat

See the implementation details with <a href="https://github.com/Pranav-Nagpure/Face-Swapping-NB.git">IPython Notebook</a>
</p>

## __Getting Started__

This Project is Built With [![Anaconda][anaconda-shield]][anaconda-url] [![VSCode][vscode-shield]][vscode-url] [![Render][render-shield]][render-url]

### __Installation__
To use the app on local machine, open Anaconda Prompt and run the following commands:

1. Clone the Repository
```sh
git clone https://github.com/Pranav-Nagpure/Face-Swapping.git
```

2. Change Working Directory
```sh
cd Face-Swapping
```

3. If needed create a Virtual Environment and activate it
```sh
conda create -n environment_name python=3.10
conda activate environment_name
```

4. Install the requirements
```sh
python -m pip install -r requirements.txt
```

5. Run the App
```sh
python app.py
```

6. Open the URL generated in a browser to use the App

7. You can use images in the sample_images folder

<p align="right">
(<a href="#readme-top">back to top</a>)
</p>

[python-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/python-shield.png "Python"
[python-url]: https://www.python.org

[html-css-js-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/html-css-js-shield.png
[html-css-js-url]: https://html.spec.whatwg.org "HTML | CSS | JavaScript"

[flask-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/flask-shield.png "Flask"
[flask-url]: https://flask.palletsprojects.com

[opencv-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/opencv-shield.png
[opencv-url]: https://opencv.org "OpenCV"

[dlib-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/dlib-shield.png
[dlib-url]: http://dlib.net "Dlib"

[anaconda-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/anaconda-shield.png
[anaconda-url]: https://www.anaconda.com "Anaconda"

[vscode-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/vscode-shield.png
[vscode-url]: https://code.visualstudio.com "VSCode"

[render-shield]: https://raw.githubusercontent.com/Pranav-Nagpure/Support-Repository/master/images/render-shield.png
[render-url]: https://render.com "Render"