$(document).ready(function(){
  
    $( document ).tooltip();
    
    $('#myblogIndex').DataTable({
      "searching": false,
      "paging": false,
      "aoColumns":[
          {"bSortable": false},
          {"bSortable": false},
          {"bSortable": true},
          {"bSortable": true},
          {"bSortable": false}
      ]
    });

    $('#blogIndex').DataTable({
      "searching": false,
      "paging": false,
      "aoColumns":[
          {"bSortable": false},
          {"bSortable": false},
          {"bSortable": true},
          {"bSortable": true},
      ]
    });
    
    $( "#accordion" ).accordion({
      collapsible: true,
    });
    $( ".widget" ).button();
    $( ".selectJui" ).selectmenu();
    $(function () {
      $('[data-toggle="tooltip"]').tooltip();
    })

    /** Select2 **/
    $("#id_category").select2();
    $("#id_blog_tags").select2({
      tags: true,
    });
  });