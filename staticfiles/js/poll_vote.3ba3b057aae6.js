document.addEventListener("DOMContentLoaded", function () {
    var pollForm = document.getElementById("pollForm");

    if (pollForm) {
        var pollVoteUrl = pollForm.dataset.voteUrl;
        var csrfToken = pollForm.dataset.csrfToken;

        pollForm.addEventListener("submit", function (event) {
            event.preventDefault();
            var formData = new FormData(this);

            fetch(pollVoteUrl, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Response data:", data);
                if (data.status === "success") {
                    alert("Vote counted!");
                    location.reload();
                } else {
                    alert("Error: " + data.message);
                }
            });
        });

        var clearChoiceBtn = document.getElementById("clearChoice");
        if (clearChoiceBtn) {
            clearChoiceBtn.addEventListener("click", function (event) {
                event.preventDefault(); // Prevent page reload
                document.querySelectorAll("input[name='option_id']").forEach(input => input.checked = false);
            });
        }
    }
});