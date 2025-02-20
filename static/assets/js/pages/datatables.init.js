// $(document).ready(function(){$("#datatable").DataTable(),$("#datatable-buttons").DataTable({lengthChange:!1,buttons:["copy","excel","pdf","colvis"]}).buttons().container().appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)"),$(".dataTables_length select").addClass("form-select form-select-sm")});

$(document).ready(function() {
    var table = $("#datatable-buttons").DataTable({
        lengthChange: false,
        buttons: [
            {
                extend: "copy",
                exportOptions: {
                    columns: ":not(:last-child)" // Exclude the last column (Action)
                }
            },
            {
                extend: "excel",
                exportOptions: {
                    columns: ":not(:last-child)"
                }
            },
            {
                extend: "pdf",
                exportOptions: {
                    columns: ":not(:last-child)"
                }
            },
            {
                extend: "colvis"
            }
        ]
    });

    // Append buttons to the right side
    table.buttons().container().appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)");

    // Style dropdown select
    $(".dataTables_length select").addClass("form-select form-select-sm");
});
