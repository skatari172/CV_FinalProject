// DOM elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const imagePreviewSection = document.getElementById('imagePreviewSection');
const previewImage = document.getElementById('previewImage');
const processBtn = document.getElementById('processBtn');
const clearBtn = document.getElementById('clearBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const latexCode = document.getElementById('latexCode');
const latexRendered = document.getElementById('latexRendered');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');

let currentFile = null;

// Upload area click handler
uploadArea.addEventListener('click', () => {
    imageInput.click();
});

// File input change handler
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
});

// Drag and drop handlers
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFile(file);
    } else {
        showError('Please drop an image file');
    }
});

// Handle file selection
function handleFile(file) {
    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please select an image file (PNG, JPG, JPEG, GIF, BMP)');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File size too large. Maximum size is 16MB');
        return;
    }

    currentFile = file;
    
    // Hide error and results
    hideError();
    hideResults();

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        imagePreviewSection.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Process button click handler
processBtn.addEventListener('click', async () => {
    if (!currentFile) {
        showError('Please select an image first');
        return;
    }

    hideError();
    hideResults();
    loadingSection.style.display = 'block';
    processBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('image', currentFile);

        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data.latex);
        } else {
            showError(data.error || 'An error occurred while processing the image');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        loadingSection.style.display = 'none';
        processBtn.disabled = false;
    }
});

// Clear button click handler
clearBtn.addEventListener('click', () => {
    currentFile = null;
    imageInput.value = '';
    imagePreviewSection.style.display = 'none';
    hideResults();
    hideError();
});

// Copy button click handler
copyBtn.addEventListener('click', () => {
    const text = latexCode.textContent;
    navigator.clipboard.writeText(text).then(() => {
        copyBtn.textContent = 'Copied!';
        setTimeout(() => {
            copyBtn.textContent = 'Copy';
        }, 2000);
    }).catch(err => {
        showError('Failed to copy to clipboard');
    });
});

// Display results
function displayResults(latex) {
    // Display LaTeX code
    latexCode.textContent = latex;
    
    // Display rendered LaTeX using MathJax
    // Wrap in display math delimiters
    const wrappedLatex = `\\[${latex}\\]`;
    latexRendered.innerHTML = wrappedLatex;
    
    // Trigger MathJax to render
    if (window.MathJax) {
        MathJax.typesetPromise([latexRendered]).catch((err) => {
            console.error('MathJax rendering error:', err);
            latexRendered.innerHTML = `<p style="color: #f44336;">Error rendering LaTeX. Raw output: ${latex}</p>`;
        });
    }
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

// Hide error
function hideError() {
    errorSection.style.display = 'none';
}

// Hide results
function hideResults() {
    resultsSection.style.display = 'none';
}

