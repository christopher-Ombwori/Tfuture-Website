(function($) {
    $(document).ready(function() {
        // Function to toggle subcategory field visibility
        function toggleSubcategoryField() {
            var category = $('#id_category').val();
            var subcategoryField = $('.field-subcategory');
            var subcategoryInput = $('#id_subcategory');
            
            // Categories that require subcategory
            var categoriesRequiringSubcategory = ['brand-identity', 'communication-kits'];
            
            if (categoriesRequiringSubcategory.includes(category)) {
                // Show subcategory field and make it required
                subcategoryField.show();
                subcategoryInput.prop('required', true);
                subcategoryInput.prop('disabled', false);
                subcategoryInput.removeClass('error');
                $('.field-subcategory .help').text('Subcategory is required for this project type.');
            } else {
                // Hide subcategory field, clear value, and make it not required
                subcategoryField.hide();
                subcategoryInput.prop('required', false);
                subcategoryInput.prop('disabled', true);
                subcategoryInput.val('');
                subcategoryInput.removeClass('error');
                $('.field-subcategory .help').text('This project type does not accept subcategories.');
            }
        }
        
        // Initial call to set up the form
        toggleSubcategoryField();
        
        // Listen for changes to the category field
        $('#id_category').on('change', function() {
            toggleSubcategoryField();
        });
        
        // Prevent form submission if subcategory is selected for unsupported categories
        $('form').on('submit', function(e) {
            var category = $('#id_category').val();
            var subcategory = $('#id_subcategory').val();
            var categoriesRequiringSubcategory = ['brand-identity', 'communication-kits'];
            
            if (!categoriesRequiringSubcategory.includes(category) && subcategory) {
                e.preventDefault();
                alert('Error: ' + $('#id_category option:selected').text() + ' projects do not accept subcategories. Please remove the subcategory selection.');
                return false;
            }
        });
    });
})(django.jQuery); 