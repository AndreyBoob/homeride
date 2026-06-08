document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.querySelector('input[name="phone"]');
    
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Удаляем все нецифровые символы
            
            // Если начинается с 8, заменяем на 7
            if (value.startsWith('8')) {
                value = '7' + value.slice(1);
            }
            
            // Если начинается с 9 и длина > 10, значит забыли +7
            if (value.startsWith('9') && value.length === 10) {
                value = '7' + value;
            }
            
            // Если начинается не с 7, добавляем 7
            if (value.length > 0 && !value.startsWith('7')) {
                value = '7' + value;
            }
            
            // Форматируем: +7 (999) 999-99-99
            let formattedValue = '+';
            if (value.length > 0) {
                formattedValue += value.charAt(0);
            }
            if (value.length > 1) {
                formattedValue += ' (' + value.substring(1, 4);
            }
            if (value.length > 4) {
                formattedValue += ') ' + value.substring(4, 7);
            }
            if (value.length > 7) {
                formattedValue += '-' + value.substring(7, 9);
            }
            if (value.length > 9) {
                formattedValue += '-' + value.substring(9, 11);
            }
            
            e.target.value = formattedValue;
        });
        
        // При потере фокуса проверяем длину
        phoneInput.addEventListener('blur', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length !== 11) {
                // Показываем ошибку если номер неполный
                e.target.setCustomValidity('Номер телефона должен содержать 11 цифр');
            } else {
                e.target.setCustomValidity('');
            }
        });
    }
});