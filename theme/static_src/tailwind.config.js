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
                    200: '#fbd0d5',
                    300: '#f7aab3',
                    400: '#f27688',
                    500: '#e94865',
                    600: '#d82d4b',
                    700: '#be1931',
                    800: '#9f172a',
                    900: '#851929'
                },
                secondary: {
                    50: '#f5f5f5',
                    100: '#e9e9e9',
                    200: '#d9d9d9',
                    300: '#c4c4c4',
                    400: '#9d9d9d',
                    500: '#7b7b7b',
                    600: '#555555',
                    700: '#434343',
                    800: '#333333',
                    900: '#1f1f1f'
                },
                tertiary: {
                    50: '#f0f9f6',
                    100: '#d9f0e8',
                    200: '#b5e0d1',
                    300: '#8ccbb5',
                    400: '#5eb193',
                    500: '#429777',
                    600: '#34785f',
                    700: '#2d614f',
                    800: '#284e42',
                    900: '#234139'
                }
            },
        },
    },
    plugins: [
        require('flowbite/plugin'),
    ],
}
