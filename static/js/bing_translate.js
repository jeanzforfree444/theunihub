document.addEventListener("DOMContentLoaded", function () {
    const apiKey = document.getElementById("translator-api-key").dataset.key;
    const endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0";
    const languageSelect = document.getElementById("language-select");

    languageSelect.addEventListener("change", function () {
        let targetLang = languageSelect.value;
        let textNodes = getTextNodes(document.body);
        let textArray = textNodes.map(node => node.nodeValue);

        if (textArray.length > 0) {
            translateText(textArray, targetLang).then(translations => {
                translations.forEach((translatedText, index) => {
                    textNodes[index].nodeValue = translatedText;
                });
            });
        }
    });

    function getTextNodes(element) {
        let walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
        let textNodes = [];
        while (walker.nextNode()) {
            textNodes.push(walker.currentNode);
        }
        return textNodes;
    }

    async function translateText(textArray, targetLang) {
        let body = textArray.map(text => ({ Text: text }));

        let response = await fetch(endpoint + `&to=${targetLang}`, {
            method: "POST",
            headers: {
                "Ocp-Apim-Subscription-Key": apiKey,
                "Ocp-Apim-Subscription-Region": "centralus",
                "Content-type": "application/json"
            },
            body: JSON.stringify(body)
        });

        let data = await response.json();
        return data.map(item => item.translations[0].text);
    }
});