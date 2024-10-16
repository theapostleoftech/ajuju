module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */
        
        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',
        
        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',
        
        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',
        
        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',
        './node_modules/flowbite/**/*.js',
        
        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#fef2f3',
                    100: '#fde6e7',
                    200: '#fbc1c5',
                    300: '#f79ca3',
                    400: '#f15f6b',
                    500: '#e63946',
                    600: '#d42836',
                    700: '#b31e2a',
                    800: '#931922',
                    900: '#7a161d'
                },
                secondary: {
                    50: '#f2f9fa',
                    100: '#e6f3f4',
                    200: '#cee7e9',
                    300: '#a8dadc',
                    400: '#7ec5c8',
                    500: '#5aaeb2',
                    600: '#458e92',
                    700: '#3b7578',
                    800: '#325d60',
                    900: '#2a4d4f'
                },
                tertiary: {
                    50: '#f2f6fa',
                    100: '#e3edf5',
                    200: '#c7dbeb',
                    300: '#9bbdda',
                    400: '#6a9ac3',
                    500: '#457b9d',
                    600: '#3d6886',
                    700: '#355870',
                    800: '#2d4a5d',
                    900: '#263e4e'
                },
                accent: {
                    50: '#f2f5f9',
                    100: '#e3eaf2',
                    200: '#c7d5e6',
                    300: '#9bb5d3',
                    400: '#6a8db8',
                    500: '#456a94',
                    600: '#395679',
                    700: '#314765',
                    800: '#2a3c55',
                    900: '#1d3557'
                },
                light: {
                    50: '#ffffff',
                    100: '#fdfefe',
                    200: '#fbfdfd',
                    300: '#f8fcfb',
                    400: '#f5faf8',
                    500: '#f1faee',
                    600: '#d1edc5',
                    700: '#afdfa0',
                    800: '#8bcf7b',
                    900: '#69be5a'
                }
            },
        },
    },
    plugins: [
        require('flowbite/plugin'),
    ],
}
