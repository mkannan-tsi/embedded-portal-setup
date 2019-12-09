function exportPDF() {
    viz.showExportPDFDialog();
    // $('.tab-dialog')[0].animate({ 'marginLeft': "-=50px" });
}

function exportData() {
    viz.showExportDataDialog();
}

function resetViz() {
    viz.revertAllAsync();
}

function showVizButtons() {
    var sheets = workbook.getActiveSheet();

    var divIndividualButtons = $('#vizButtons');

    // First clear any buttons that may have been added on a previous load
    divIndividualButtons.html("");
    // Show 'standard' controls, common to all vizzes
    divIndividualButtons.append('<button type="button" onclick="resetViz()" class="btn btn-primary col-xs-3"  style="min-width:135px; margin-right: 5px; margin-top: 5px;">Reset Filters</button>');
    divIndividualButtons.append('<button type="button" onclick="exportPDF()" class="btn btn-primary col-xs-3" style="min-width:135px; margin-right: 5px; margin-top: 5px;">Export PDF</button>');
    divIndividualButtons.append('<button type="button" onclick="exportData()" class="btn btn-primary col-xs-3" style="min-width:135px; margin-right: 5px; margin-top: 5px;">Export Data</button>');
    divIndividualButtons.append('<button type="button" onclick="launch_edit()" class="btn btn-primary col-xs-3" style="min-width:135px; margin-right: 5px; margin-top: 5px;">Edit</button>');

    // if (sheets.getSheetType() === "dashboard")
    // {
    //    var dashboard = sheets.getWorksheets(); 
    // // Only show buttons to switch vizzes if there's more than one
    //     if (dashboard.length > 1) {
    //         divIndividualButtons.append('<br> <br>');
    //         for (var sheetIndex = 0; sheetIndex < dashboard.length; sheetIndex++) {
    //             var sheet = dashboard[sheetIndex];
    //             console.log (sheet.getName());
    //             divIndividualButtons.append('<button type="button" onclick="switchToViz(\'' + sheet.getName() + '\')" class="btn btn-primary col-xs-3" style="min-width:135px; margin-right: 5px; margin-top: 5px;">See ' + sheet.getName() + '</button>')
    //         }
    //     }
    // }
}

// function switchToViz(vizName) {
//     console.log (vizName);
//     if (viz) {
//         viz.dispose();
//     }
//     var index = url.lastIndexOf("/");
//     url = url.substring (0, index+1) + vizName
//     viz = new tableau.Viz(placeholderDiv, url, options); 
//     // workbook.activateSheetAsync(vizName).then(function (dashboard) {

//     //     dashboard.changeSizeAsync({
//     //         behavior: tableau.SheetSizeBehavior.AUTOMATIC
//     //     });
//     // });
// }

function resetAllMarks() {
    
    var referrer = viz.getWorkbook().getActiveSheet();

    if (referrer.getSheetType() == "dashboard") {
        // The active sheets is a dashboard, which is made of several sheets
        var sheets = referrer.getWorksheets();

        // Iterate over the sheets until we find the correct one and clear the marks
        for (var sheetIndex = 0; sheetIndex < sheets.length; sheetIndex++) {
            if (sheets[sheetIndex].getName() == nameOfVizToInteract) {
                sheets[sheetIndex].clearSelectedMarksAsync();
            }
        }
    }
    else {
        // This is not a dashboard so just clear the sheet's selection
        referrer.clearSelectedMarksAsync();
    }

    $('#eventBox').hide(800);
    $('#eventPanel').html("");
}

function launch_edit() {
    // Adjust UI: Hide Buttons & navigation menu, increase size for edit mode
    $('#VizToolbar').hide();
    $('body').addClass("sidebar-collapse");
    $(".content-wrapper").css("height","1200px");
    
    viz.getCurrentUrlAsync().then(function(current_url){
        edit_url = current_url.split('?')[0].replace('/views', '/authoring');                  
          edit_options = {
              height:"800px",
              width: "1200px",
              onFirstInteractive: function () {
                  var iframe = document.querySelectorAll('iframe')[0];
                  iframe.onload = function(){
                      // Getting the URL post exit from web edit window
                      viz.getCurrentUrlAsync().then(function(current_url){
                          viz_url = current_url.split('?')[0];
                      }).then(function(){
                          $('#VizToolbar').show();
                          $('body').removeClass("sidebar-collapse");
                          $(".content-wrapper").css("height", "");
                          loadViz (placeholderDiv, viz_url, options)
                      })
                  }
              }
          };
    loadViz (placeholderDiv, edit_url, edit_options);          
    });  
}

function loadViz (placeholderDiv, url, options) {
   if (viz) {
       viz.dispose();
   }
   viz = new tableau.Viz(placeholderDiv, url, options);
}

function completeLoad() {
    // Once the workbook & viz have loaded, assign them to global variables
    workbook = viz.getWorkbook();
    activeSheet = workbook.getActiveSheet();
    // Load custom controls based on the vizzes published to the server
    showVizButtons();

}

$(document).ready(initializeViz); 