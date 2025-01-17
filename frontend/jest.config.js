module.exports = {
    moduleNameMapper: {
        '\\.(css|less|sass|scss)$': 'identity-obj-proxy',
    },
    transform: {
        '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest',
    },
    transformIgnorePatterns: [
        'node_modules/(?!(react-toastify)/)', // Add the problematic package here
    ],
    collectCoverageFrom: [
        "src/**/*.{js,jsx,ts,tsx}", // Include source files
        "!src/index.js", // Exclude entry point if needed
        "!src/reportWebVitals.js",
        "!src/setupTests.js",
        "!**/node_modules/**", // Exclude dependencies
        "!src/serviceWorker.js", // Exclude other non-test files
    ],
    testEnvironment: "jsdom",
    setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],
};
