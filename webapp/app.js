async function search() {
    const product = document.getElementById("product").value;

    const res = await fetch(
        `http://127.0.0.1:8000/api/prices?product=${product}`
    );
    const data = await res.json();

    let html = "";
    data.forEach(item => {
        html += `<p><b>${item.site}:</b> ${item.price ? item.price + " TL" : "Fiyat bulunamadı"}</p>`;
    });

    document.getElementById("results").innerHTML = html;
}