var src_img_upload = document.getElementById('src_img_upload');
var dest_img_upload = document.getElementById('dest_img_upload');

var src_img = document.getElementById('src_img');
var dest_img = document.getElementById('dest_img');
var result_img = document.getElementById('result_img');

function img_disable(img) {
  if (img.getAttribute('src') == '') {
    img.style.display = 'none';
  }
  else {
    img.style.display = 'block';
  }
}

function submit_button_disable() {
  if (src_img_upload.value != '' && dest_img_upload.value != '') {
    submit_button.disabled = false;
  }
  else {
    submit_button.disabled = true;
  }
}

src_img_upload.onchange = function () {
  if (src_img_upload.value == '') {
    src_img.setAttribute('src', '');
  }
  else {
    src_img.setAttribute('src', URL.createObjectURL(src_img_upload.files[0]));
  }

  img_disable(src_img);
  submit_button_disable();
}

dest_img_upload.onchange = function () {
  if (dest_img_upload.value == '') {
    dest_img.setAttribute('src', '');
  }
  else {
    dest_img.setAttribute('src', URL.createObjectURL(dest_img_upload.files[0]));
  }

  img_disable(dest_img);
  submit_button_disable();
}

const images = [src_img, dest_img, result_img];
for (let i = 0; i < images.length; i++) {
  img_disable(images[i]);
}
