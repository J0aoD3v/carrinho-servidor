/**
 * Excalidraw Lazy Loader
 * This script enables lazy loading of Excalidraw drawing data to improve performance.
 * Drawing data is loaded only when needed (e.g., when switching to Excalidraw view).
 */

class ExcalidrawLazyLoader {
    constructor() {
        this.index = null;
        this.cache = new Map();
        this.loadIndex();
    }

    async loadIndex() {
        try {
            const response = await fetch('.excalidraw/index.json');
            this.index = await response.json();
            console.log('Excalidraw index loaded:', Object.keys(this.index).length, 'files');
        } catch (error) {
            console.warn('Could not load Excalidraw index:', error);
        }
    }

    async loadDrawingData(drawingHash) {
        // Check cache first
        if (this.cache.has(drawingHash)) {
            return this.cache.get(drawingHash);
        }

        try {
            const response = await fetch(`.excalidraw/${drawingHash}.excalidraw`);
            const drawingData = await response.text();
            
            // Cache the data
            this.cache.set(drawingHash, drawingData);
            
            return drawingData;
        } catch (error) {
            console.error('Failed to load drawing data:', drawingHash, error);
            return null;
        }
    }

    async restoreDrawingForFile(filePath) {
        if (!this.index || !this.index[filePath]) {
            console.warn('No drawing data found for file:', filePath);
            return false;
        }

        const drawingInfo = this.index[filePath];
        const drawingData = await this.loadDrawingData(drawingInfo.drawing_hash);
        
        if (!drawingData) {
            return false;
        }

        // Find and replace drawing references in the current document
        const content = document.body.innerHTML;
        const referencePattern = new RegExp(
            `(<!-- DRAWING_REFERENCE: ${drawingInfo.drawing_hash} -->)`,
            'g'
        );

        const updatedContent = content.replace(referencePattern, drawingData);
        
        if (updatedContent !== content) {
            document.body.innerHTML = updatedContent;
            console.log('Drawing data restored for:', filePath);
            return true;
        }

        return false;
    }

    // Auto-detect current file and restore drawing if needed
    async autoRestoreCurrentFile() {
        // This would be called by Obsidian when switching to Excalidraw view
        // The actual implementation would depend on Obsidian's plugin API
        const currentFile = this.getCurrentFileName();
        if (currentFile) {
            await this.restoreDrawingForFile(currentFile);
        }
    }

    getCurrentFileName() {
        // This is a placeholder - in a real Obsidian plugin, this would
        // use the Obsidian API to get the current active file
        const path = window.location.pathname;
        return path.substring(path.lastIndexOf('/') + 1);
    }

    // Get performance statistics
    getPerformanceStats() {
        if (!this.index) return null;

        const stats = {
            totalFiles: Object.keys(this.index).length,
            totalOriginalSize: 0,
            cachedFiles: this.cache.size,
            memoryUsage: 0
        };

        for (const fileInfo of Object.values(this.index)) {
            stats.totalOriginalSize += fileInfo.size_bytes;
        }

        for (const data of this.cache.values()) {
            stats.memoryUsage += data.length;
        }

        return stats;
    }
}

// Global instance
if (typeof window !== 'undefined') {
    window.excalidrawLazyLoader = new ExcalidrawLazyLoader();
    
    // Auto-restore when document is ready
    document.addEventListener('DOMContentLoaded', () => {
        window.excalidrawLazyLoader.autoRestoreCurrentFile();
    });
}

// Export for Node.js/module environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ExcalidrawLazyLoader;
}