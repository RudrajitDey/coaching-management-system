document.addEventListener('DOMContentLoaded', function() {
    const roleSelect = document.querySelector('#id_role');
    const salarySection = document.querySelector('.salary-section');
    const feesSection = document.querySelector('.fees-section');
    
    function toggleFieldsets() {
        const role = roleSelect ? roleSelect.value : '';
        
        if (salarySection) {
            if (role === 'teacher') {
                salarySection.style.display = 'block';
            } else {
                salarySection.style.display = 'none';
            }
        }
        
        if (feesSection) {
            if (role === 'student') {
                feesSection.style.display = 'block';
            } else {
                feesSection.style.display = 'none';
            }
        }
    }
    
    if (roleSelect) {
        roleSelect.addEventListener('change', toggleFieldsets);
        toggleFieldsets(); // Initial state
    }
});
