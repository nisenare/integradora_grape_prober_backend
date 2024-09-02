const madurez_es = {
    "Inmature": "Inmadura",
    "Semi Mature": "Semi Madura",
    "Mature": "Madura"
}


let thumbnail_clicked_first_time = false;


function setThumbnailImage(id, annotated_image) {
    let img_element = document.getElementById('image_' + id);
    img_element.src = 'data:image/png;base64,' + annotated_image;
}


function setPredictionInfo(date_time, annotated_image, overall_maturity, ph) {
    thumbnail_clicked_first_time = true;
    let image_detail = document.getElementById('image_detail');
    let fecha_detail = document.getElementById('fecha_detail');
    let madurez_detail = document.getElementById('madurez_detail');
    let ph_detail = document.getElementById('ph_detail');

    image_detail.src = 'data:image/png;base64,' + annotated_image;
    date_time = date_time.split(', ')
    fecha_detail.textContent = date_time[0] + ", " + date_time[1] + " a las " + date_time[2];
    madurez_detail.textContent = " " + madurez_es[overall_maturity];
    ph_detail.textContent = " " + ph;
    
    if (thumbnail_clicked_first_time) {
        let details = document.getElementById("details")
        details.style.visibility = "visible";
    }

}

