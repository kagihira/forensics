const API_BASE = window.location.origin.replace("5500", "8001");

// 🔹 Функция загрузки E01 файла
document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let fileInput = document.getElementById("e01File");
    let deviceId = document.getElementById("deviceId").value;
    let resultContainer = document.getElementById("uploadResult");
    
    if (!fileInput.files.length) {
        resultContainer.innerText = "⚠️ Выберите файл перед загрузкой.";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("device_id", deviceId);

    resultContainer.innerText = "⏳ Загрузка файла...";

    try {
        let response = await fetch(`${API_BASE}/upload_e01/`, {
            method: "POST",
            body: formData
        });

        let result = await response.json();
        console.log("Ответ сервера:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка загрузки файла");

        resultContainer.innerText = `✅ Файл загружен: ${result.message || "Успех"}`;
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка загрузки файла:", error);
    }
});

// 🔹 Функция извлечения текста
async function extractText() {
    let deviceId = document.getElementById("extractDeviceId").value;
    let resultContainer = document.getElementById("extractResult");
    resultContainer.innerText = "⏳ Извлекаем текст...";

    try {
        let response = await fetch(`${API_BASE}/extract_text/${deviceId}/`);
        let result = await response.json();
        console.log("Извлечённый текст:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка извлечения текста");

        resultContainer.innerText = `📄 Извлечённый текст: ${result.message || "Успех"}`;
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка извлечения текста:", error);
    }
}

// 🔹 Функция анализа текста
async function analyzeText() {
    let deviceId = document.getElementById("analyzeDeviceId").value;
    let resultContainer = document.getElementById("analyzeResult");
    resultContainer.innerText = "⏳ Анализируем текст...";

    try {
        let response = await fetch(`${API_BASE}/analyze_text/${deviceId}/`);
        let result = await response.json();
        console.log("Анализ текста:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка анализа текста");

        resultContainer.innerText = `🔍 Анализ текста: ${result.message || "Готово"}`;
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка анализа текста:", error);
    }
}

// 🔹 Функция сравнения устройств
async function compareDevices() {
    let device1 = document.getElementById("compareDevice1").value;
    let device2 = document.getElementById("compareDevice2").value;
    let resultContainer = document.getElementById("compareResult");

    resultContainer.innerText = "⏳ Сравниваем файлы...";

    try {
        let response = await fetch(`${API_BASE}/compare/?device1=${device1}&device2=${device2}`);
        let result = await response.json();
        console.log("Результаты сравнения:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка сравнения файлов");

        if (result.matches.length > 0) {
            let output = "<h3>🔍 Найдены совпадения:</h3><ul>";
            result.matches.forEach(match => {
                output += `<li>📄 ${match[0]} ⟷ 📄 ${match[1]} (Совпадение: ${(match[2] * 100).toFixed(2)}%)</li>`;
            });
            output += "</ul>";
            resultContainer.innerHTML = output;
        } else {
            resultContainer.innerText = "❌ Совпадений не найдено.";
        }
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка сравнения:", error);
    }
}

// 🔹 Функция анализа переписок
async function analyzeMessages() {
    let deviceId = document.getElementById("messagesDeviceId").value;
    let resultContainer = document.getElementById("messagesResult");

    resultContainer.innerText = "⏳ Анализируем переписку...";

    try {
        let response = await fetch(`${API_BASE}/analyze_messages/${deviceId}/`);
        let result = await response.json();
        console.log("Результаты анализа сообщений:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка анализа переписок");

        let output = "<h3>📩 Переписка:</h3><ul>";
        Object.keys(result.conversations).forEach(key => {
            output += `<li><strong>${key}</strong>:<br>${result.conversations[key].join("<br>")}</li>`;
        });
        output += "</ul>";
        resultContainer.innerHTML = output;
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка анализа сообщений:", error);
    }
}

// 🔹 Функция сортировки документов
async function sortDocuments() {
    let deviceId = document.getElementById("sortDeviceId").value;
    let resultContainer = document.getElementById("sortResult");

    resultContainer.innerText = "⏳ Сортируем документы...";

    try {
        let response = await fetch(`${API_BASE}/sort_documents/${deviceId}/`);
        let result = await response.json();
        console.log("Сортировка документов:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка сортировки документов");

        let output = "<h3>📂 Сортировка:</h3>";
        output += "<h4 style='color: red;'>⚠️ Опасные документы:</h4><ul>";
        result.sorted_documents.dangerous.forEach(file => {
            output += `<li>${file}</li>`;
        });
        output += "</ul>";

        output += "<h4 style='color: green;'>✅ Безопасные документы:</h4><ul>";
        result.sorted_documents.safe.forEach(file => {
            output += `<li>${file}</li>`;
        });
        output += "</ul>";

        resultContainer.innerHTML = output;
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка сортировки:", error);
    }
}

// 🔹 Функция поиска связей между пользователями
async function findConnections() {
    let deviceId = document.getElementById("connectionsDeviceId").value;
    let resultContainer = document.getElementById("connectionsResult");

    resultContainer.innerText = "⏳ Анализируем связи...";

    try {
        let response = await fetch(`${API_BASE}/find_connections/${deviceId}/`);
        let result = await response.json();
        console.log("Связи между пользователями:", result);

        if (!response.ok) throw new Error(result.error || "Ошибка анализа связей");

        let output = "<h3>🔗 Найденные связи:</h3><ul>";
        Object.keys(result.connections).forEach(user => {
            output += `<li><strong>${user}</strong> связан с: ${result.connections[user].join(", ")}</li>`;
        });
        output += "</ul>";
        resultContainer.innerHTML = output;
    } catch (error) {
        resultContainer.innerText = `❌ Ошибка: ${error.message}`;
        console.error("Ошибка анализа связей:", error);
    }
}
