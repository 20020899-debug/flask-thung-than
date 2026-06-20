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
