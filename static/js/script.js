document.addEventListener('DOMContentLoaded', () => {
    // Navbar toggle functionality
    const navbarToggle = document.getElementById('navbar-toggle');
    const navbarMenu = document.querySelector('.navbar-menu');
    
    if (navbarToggle) {
        navbarToggle.addEventListener('click', () => {
            navbarMenu.classList.toggle('active');
        });
    }
    
    // Close navbar when clicking outside
    document.addEventListener('click', (e) => {
        if (navbarMenu.classList.contains('active') && 
            !e.target.closest('.navbar-menu') && 
            !e.target.closest('#navbar-toggle')) {
            navbarMenu.classList.remove('active');
        }
    });

    // Navigation scrolling
    const aboutLink = document.querySelector('.navbar-item:not(.active) a');
    const converterBox = document.querySelector('.converter-box');
    const aboutSection = document.querySelector('.about-section');
    const activeNavItem = document.querySelector('.navbar-item.active');
    const imageConverterLink = document.querySelector('.navbar-item.active a');
    
    // Handle About link click
    if (aboutLink) {
        aboutLink.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active nav item
            activeNavItem.classList.remove('active');
            aboutLink.parentElement.classList.add('active');
            
            // Smooth scroll to about section
            aboutSection.scrollIntoView({ behavior: 'smooth' });
        });
    }
    
    // Handle Image Converter link click
    if (imageConverterLink) {
        imageConverterLink.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Update active nav item
            aboutLink.parentElement.classList.remove('active');
            imageConverterLink.parentElement.classList.add('active');
            
            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // File upload and conversion functionality
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const outputFormat = document.getElementById('outputFormat');
    const convertBtn = document.getElementById('convertBtn');
    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const clearBtn = document.getElementById('clearBtn');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const notification = document.getElementById('notification');
    const downloadBtn = document.getElementById('downloadBtn');
    const downloadSection = document.getElementById('downloadSection');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    // Handle file input change
    fileInput.addEventListener('change', handleFileSelect, false);

    // Handle browse button click
    document.querySelector('.browse-btn').addEventListener('click', () => {
        fileInput.click();
    });

    // Handle clear button click
    clearBtn.addEventListener('click', clearFile);

    // Handle output format change
    outputFormat.addEventListener('change', updateConvertButton);

    // Handle convert button click
    convertBtn.addEventListener('click', handleConversion);

    function showNotification(message, type = 'success') {
        notification.textContent = message;
        notification.className = `notification ${type} show`;
        setTimeout(() => {
            notification.className = 'notification';
        }, 3000);
    }

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            handleFiles(files);
        }
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            handleFiles(files);
        }
    }

    function handleFiles(files) {
        const file = files[0];
        fileName.textContent = file.name;
        fileInfo.style.display = 'block';
        fileInfo.classList.add('slide-in');
        downloadSection.style.display = 'none';
        updateConvertButton();
    }

    function clearFile() {
        fileInput.value = '';
        fileName.textContent = '';
        fileInfo.classList.remove('slide-in');
        fileInfo.classList.add('slide-out');
        setTimeout(() => {
            fileInfo.style.display = 'none';
            fileInfo.classList.remove('slide-out');
        }, 300);
        downloadSection.style.display = 'none';
        updateConvertButton();
    }

    function updateConvertButton() {
        const hasFile = fileInput.files.length > 0 || fileName.textContent !== '';
        const hasFormat = outputFormat.value !== '';
        convertBtn.disabled = !(hasFile && hasFormat);
    }

    async function handleConversion() {
        const file = fileInput.files[0];
        const format = outputFormat.value;

        if (!file || !format) {
            showNotification('Please select a file and output format', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);
        formData.append('output_format', format);

        loadingOverlay.style.display = 'flex';
        loadingOverlay.classList.add('fade-in');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showNotification('File converted successfully');
                downloadSection.style.display = 'block';
                downloadSection.classList.add('slide-in');
                downloadBtn.href = `/download/${data.filename}`;
                downloadBtn.download = `converted.${format}`;
            } else {
                showNotification(data.error || 'Error converting file', 'error');
            }
        } catch (error) {
            showNotification('Error converting file', 'error');
            console.error('Error:', error);
        } finally {
            loadingOverlay.classList.remove('fade-in');
            loadingOverlay.classList.add('fade-out');
            setTimeout(() => {
                loadingOverlay.style.display = 'none';
                loadingOverlay.classList.remove('fade-out');
            }, 300);
        }
    }
}); 