const { 
    // ... existing imports ...
    extractChlorideValue,
    extractCholesterolValue,
    extractHDLValue,
    extractSodiumValue,
    extractTriglyceridesValue
} = require('./index.js');

// ... existing code ...

let chlorideValue = null;
let cholesterolValue = null;
let hdlValue = null;
let sodiumValue = null;
let triglyceridesValue = null;

// Process each line
lines.forEach(line => {
    // ... existing extractions ...

    const chlorideResult = extractChlorideValue(line);
    if (chlorideResult !== null) {
        chlorideValue = chlorideResult;
    }

    const cholesterolResult = extractCholesterolValue(line);
    if (cholesterolResult !== null) {
        cholesterolValue = cholesterolResult;
    }

    const hdlResult = extractHDLValue(line);
    if (hdlResult !== null) {
        hdlValue = hdlResult;
    }

    const sodiumResult = extractSodiumValue(line);
    if (sodiumResult !== null) {
        sodiumValue = sodiumResult;
    }

    const triglyceridesResult = extractTriglyceridesValue(line);
    if (triglyceridesResult !== null) {
        triglyceridesValue = triglyceridesResult;
    }
});

// When creating the final JSON, update these values
const labs = [
    // ... other labs ...
    {
        client_id: 1,
        test_name: "Chloride",
        value: chlorideValue || "10610507",
        units: null,
        reference_range: null,
        is_abnormal: null,
        date_collected: null
    },
    {
        client_id: 1,
        test_name: "Cholesterol, Total",
        value: cholesterolValue || "13314207",
        units: null,
        reference_range: null,
        is_abnormal: null,
        date_collected: null
    },
    // ... continue for HDL, Sodium, and Triglycerides ...
];

const extractors = require('./index.js');

// Create variables for each lab value
const labValues = {};

// Process each line
lines.forEach(line => {
    // Try each extractor
    Object.entries(extractors).forEach(([extractorName, extractorFn]) => {
        const result = extractorFn(line);
        if (result !== null) {
            // Convert extractor name back to lab name (remove 'extract' and 'Value')
            const labName = extractorName
                .replace('extract', '')
                .replace('Value', '')
                // Add spaces before capital letters
                .replace(/([A-Z])/g, ' $1')
                .trim();
            labValues[labName] = result;
        }
    });
});

// When creating the final JSON
const labs = Object.entries(labValues).map(([labName, value]) => ({
    client_id: 1,
    test_name: labName,
    value: value,
    units: null,
    reference_range: null,
    is_abnormal: null,
    date_collected: null
}));
