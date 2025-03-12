document.addEventListener("DOMContentLoaded", function () {
    let totalForms = document.getElementById("id_form-TOTAL_FORMS");
    let optionContainer = document.getElementById("poll-options");
    let addOptionBtn = document.getElementById("add-option-btn");
    let minOptions = 2;
    let maxOptions = 5;

    function updateButtons() {
        let currentCount = optionContainer.children.length;
        addOptionBtn.style.display = currentCount >= maxOptions ? "none" : "inline-block";

        document.querySelectorAll(".remove-option-btn").forEach((btn) => {
            btn.style.display = currentCount > minOptions ? "inline-block" : "none";
        });
    }

    function createOptionField(index) {
        let newOption = document.createElement("div");
        newOption.classList.add("poll-option", "d-flex", "align-items-center", "mb-2"); 

        newOption.innerHTML = `
            <input type="text" name="form-${index}-option_text" id="id_form-${index}-option_text" 
                   class="form-control me-2" placeholder="Enter option..." required>
            <button type="button" class="ml-3 btn btn-danger btn-sm remove-option-btn">
                <span data-feather="minus-circle"></span>
            </button>
        `;

        newOption.querySelector(".remove-option-btn").addEventListener("click", function () {
            newOption.remove();
            totalForms.value = optionContainer.children.length;  
            updateButtons();
        });

        return newOption;
    }

    addOptionBtn.addEventListener("click", function () {
        let currentCount = optionContainer.children.length;

        if (currentCount < maxOptions) {
            let newIndex = currentCount; 
            let newOption = createOptionField(newIndex);
            
            optionContainer.appendChild(newOption);

            totalForms.value = optionContainer.children.length;

            updateButtons();
            feather.replace();
        }
    });

    updateButtons();
    feather.replace();
});