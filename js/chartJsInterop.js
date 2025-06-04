// ChartJs Interop for Blazor
window.chartJsInterop = {
    setupCharts: function () {
        // Make sure Chart.js is loaded
        if (typeof Chart === 'undefined') {
            console.error('Chart.js is not loaded!');
            return false;
        }
        
        // Clear any existing charts to prevent ID conflicts
        Chart.helpers.each(Chart.instances, function(instance) {
            instance.destroy();
        });
        
        console.log('Chart.js interop initialized successfully');
        return true;
    }
};
