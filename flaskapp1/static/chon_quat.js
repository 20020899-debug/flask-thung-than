async function timQuat() {

    const D =
    parseFloat(
        document.getElementById("diameter").value
    );

    const V =
    parseFloat(
        document.getElementById("velocity").value
    );

    const P =
    parseFloat(
        document.getElementById("pressure").value
    ) || 0;

    const loai =
        document.getElementById("loaiQuat").value;

    if (!D || !V) {

        alert("Nhập đường kính và vận tốc");

        return;
    }

    // mm -> m
    const d = D / 1000;

    // m3/h
    const Q =
        Math.PI *
        d *
        d /
        4 *
        V *
        3600;

    const res =
        await fetch(
            `/tim_quat?q=${Q}&p=${P}&loai=${encodeURIComponent(loai)}`
        );

    const fans =
        await res.json();

    let html = `
        <h3>
            Lưu lượng tính toán:
            ${Math.round(Q).toLocaleString()}
            m³/h
        </h3>
    `;

    if (fans.length === 0) {

        html += `
            <p>
                Không tìm thấy quạt phù hợp
            </p>
        `;

    } else {

        fans.forEach(fan => {

            html += `
                <div class="fan-card">

                    <h3>${fan.Model}</h3>
                    <button
                    onclick="
                    goiYHeThong(
                    ${fan.Qmin},
                    ${fan.Qmax}
                    )">
                    Chọn thiết bị phù hợp
                    </button>

                    <p>
                        Loại:
                        ${fan.Loai}
                    </p>

                    <p>
                        Lưu lượng:
                        ${fan.Qmin.toLocaleString()}
                        -
                        ${fan.Qmax.toLocaleString()}
                        m³/h
                    </p>

                    <p>
                        Áp suất:
                        ${fan.Pmin.toLocaleString()}
                        -
                        ${fan.Pmax.toLocaleString()}
                        Pa
                    </p>

                    <p>
                        Công suất:
                        ${fan.Kw} kW
                    </p>

                </div>
            `;
        });
    }

    document.getElementById("result").innerHTML =
        html;
}



async function goiYHeThong(
    qmin,
    qmax
){

    const res =
    await fetch(
        `/goi_y_he_thong?qmin=${qmin}&qmax=${qmax}`
    );

    const data =
        await res.json();

    let html = "";

    html += "<h2>Cyclone phù hợp</h2>";

    data.cyclone.forEach(item => {

        html += `
        <div class="fan-card">
            ${item.Model}
            (${item.Q.toLocaleString()} m³/h)
        </div>
        `;
    });

    html += "<h2>Tháp lọc phù hợp</h2>";

    data.thap.forEach(item => {

        html += `
        <div class="fan-card">
            ${item.Model}
            (${item.Q.toLocaleString()} m³/h)
        </div>
        `;
    });

    html += "<h2>Thùng than phù hợp</h2>";

    data.than.forEach(item => {

        html += `
        <div class="fan-card">
            ${item.Model}
            (${item.Q.toLocaleString()} m³/h)
        </div>
        `;
    });

    document.getElementById(
        "result"
    ).innerHTML += html;
}
