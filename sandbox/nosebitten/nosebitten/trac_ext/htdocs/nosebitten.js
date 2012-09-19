$(document).ready(function() {
    $("#nosebitten_coverage").tableSorter({
        sortColumn: 'Unit',         // Integer or String of the name of the column to sort by.
        sortClassAsc: 'sortUp',       // class name for ascending sorting action to header
        sortClassDesc: 'sortDown',    // class name for descending sorting action to header
        headerClass: 'largeHeaders',           // class name for headers (th's)
        disableHeader: ['Missed Lines'],
    });
});
