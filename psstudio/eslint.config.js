module.exports = [
  {
    files: ["**/*.js"],
    ignores: [
      "public/dist/**",
      "public/server/editor/source/js/**",
      "utils/toolkit/static/*.js",
      "**/*.min.js"
    ],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        angular: "readonly",
        $: "readonly",
        require: "readonly",
        process: "readonly",
        module: "writable",
        exports: "writable",
        console: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        alert: "readonly",
        confirm: "readonly",
        FileReader: "readonly",
        Blob: "readonly",
        navigator: "readonly",
        jQuery: "readonly",
        ga: "readonly",
        d3: "readonly",
        google: "readonly",
        Morris: "readonly",
        Chartist: "readonly",
        moment: "readonly"
      }
    },
    rules: {
      semi: ["error", "always"],
      quotes: ["error", "double"],
      "no-unused-vars": "warn",
      "no-undef": "error",
      "no-console": "off"
    },
  },
]; 