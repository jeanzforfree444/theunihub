$(document).ready(function() {
    $('#search-input').keyup(function() {
        var query = $(this).val();
        $.get('/main/suggest/', {'suggestion': query}, function(data) {
            $('#categories-listing').html(data.categories);
            $('#forums-listing').html(data.forums);
        });
    });

    function updateProfiles() {
        var searchQuery = $('#profile-search-input').val();
        var university = $('#university-filter').val();

        $.get('/main/users/', { search: searchQuery, university: university }, function(data) {
            $('#profile-list').html(data.profiles_html);
        });
    }

    $('#profile-search-input').on('input', updateProfiles);
    $('#university-filter').change(updateProfiles);
});