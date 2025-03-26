document.addEventListener("DOMContentLoaded", function() {
    let universitySelect = document.getElementById("id_university");
    let universityDetails = document.getElementById("university-details");

    function toggleUniversityFields() {
        if (universitySelect.value) {
            universityDetails.style.display = "block";
        } else {
            universityDetails.style.display = "none";
        }
    }

    toggleUniversityFields();

    universitySelect.addEventListener("change", toggleUniversityFields);
});