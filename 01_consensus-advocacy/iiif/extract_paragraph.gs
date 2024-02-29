/*
Function to loop through each Google Doc in a single Drive folder, get all Paragraphs,
then get the Text and append to the 'Data' sheet. Adds a new Column for each Paragraph
if there is more than 1. 
From https://gist.githubusercontent.com/phillypb/a204294a8d16a47c45f391c7d139c4f4/raw/1f83b4d252bfcbbb9ef29628b2c15ccf35b70b21/Extract%20text%20from%20multiple%20Google%20Docs%20into%20a%20Sheet.gs
*/


function getParagraphs() {

  // log start of script in sheet
  logEvent('Starting script');

  // set error variable flag to true as no problems
  var noErrors = true;

  // get spreadsheet
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  // display Toast notification to inform user
  ss.toast('Running ...', 'Script starting');

  // get Welcome sheet
  var welcomeSheet = ss.getSheetByName('Welcome');


  // get Data sheet
  var dataSheet = ss.getSheetByName('Data');


  // get Google Drive Folder containing Files
  try {
    var folderID = welcomeSheet.getRange(5, 2).getValue();
    var folder = DriveApp.getFolderById(folderID);

    // get all Files in Google Drive Folder
    var files = folder.getFiles();
  }
  catch (err) {
    // log error in sheet
    logEvent('Problem getting Google Drive Folder: ' + err);

    // display user popup to inform of error
    var popupTitle = 'Google Drive Folder error';
    var popupMessage = 'Problem getting Google Drive Folder: ' + err;
    htmlPopup(popupTitle, popupMessage);

    // set error variable flag to false so rest of script stops
    var noErrors = false;
  }


  // check there have been no errors before proceeding
  if (noErrors) {

    // loop through each File in turn ********************************
    while (files.hasNext()) {

      try {
        // get last row of Data sheet to add information to
        var dataLastRow = dataSheet.getLastRow();

        // add 1 to last row to account for Header row when appending information
        var dataRow = dataLastRow + 1;

        // get the File
        var file = files.next();

        // get File name
        var fileName = file.getName();

        // get File Url
        var fileUrl = file.getUrl();

        // create hyperlink for adding to sheet later
        var hyperlink = '=HYPERLINK("' + fileUrl + '","' + fileName + '")';


        // append File information to Data sheet
        dataSheet.getRange(dataRow, 1).setValue(fileName);
        dataSheet.getRange(dataRow, 2).setValue(hyperlink);


        // open the File and get all Paragraphs
        var doc = DocumentApp.openByUrl(fileUrl);
        var body = doc.getBody();
        var paragraphs = body.getParagraphs();


        // set the Column value which starts at 3
        var column = 3;

        // loop through each Paragraph and add to Data sheet as a new Column ************
        for (var i = 0; i < paragraphs.length; i++) {

          // get the text
          var text = paragraphs[i].getText();

          // check there is text otherwise ignore blank/empty Paragraphs
          if (text == "") {
            // no text, do not increase 'column' as do not want blank Column in sheet
          }
          else {
            // there is text, add to sheet and increment 'column' to move along 1 Column
            var paragraphCell = dataSheet.getRange(dataRow, column).setValue(text);
            column++;

            // set Column to wrap text to fit content better
            paragraphCell.setWrap(true);
          }

        }
        // loop through each Paragraph and add to Data sheet as a new Column ************

      }
      catch (err) {
        // log error in sheet
        logEvent('Problem iterating through File on Row ' + dataRow + ': ' + err);

        // display user popup to inform of error
        var popupTitle = 'File error on Row ' + dataRow;
        var popupMessage = 'Problem with File: ' + err;
        htmlPopup(popupTitle, popupMessage);

        // set error variable to false so rest of script stops
        var noErrors = false;

        // break out of loop to stop script
        break;
      }

    }
    // loop through each File in turn ********************************

  }
  else {
    // error getting Google Drive Folder containing Files
  }


  // check status of error variable flag to determine final user popup
  if (noErrors) {
    // log message in sheet
    logEvent('Script completed without errors.');

    // no errors have occurred in the script
    var popupTitle = 'Script Complete';
    var popupMessage = 'There were no errors.';
    htmlPopup(popupTitle, popupMessage);
  }
  else {
    // do nothing as the above 'catches' already display a user popup

    // log message in sheet
    logEvent('Script completed with errors.');
  }



}


/*
Function to output information to the 'Log' sheet.
*/

function logEvent(action) {

  // get the user running the script
  var theUser = Session.getActiveUser().getEmail();

  // get the relevant spreadsheet to output log details
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = ss.getSheetByName('Log');

  // create and format a timestamp
  var dateTime = new Date();
  var timeZone = ss.getSpreadsheetTimeZone();
  var niceDateTime = Utilities.formatDate(dateTime, timeZone, "dd/MM/yy @ HH:mm:ss");

  // create array of data for pasting into log sheet
  var logData = [niceDateTime, theUser, action];

  // append details into next row of log sheet
  logSheet.appendRow(logData);

}


/*
Display a modal dialog box with custom HtmlService content.
Does not suspend the script.
*/

function htmlPopup(popupTitle, popupMessage) {

  var htmlOutput = HtmlService
    .createHtmlOutput(popupMessage)
    .setWidth(360)
    .setHeight(180);
  SpreadsheetApp.getUi().showModalDialog(htmlOutput, popupTitle);

}


/*
Create Menu item for running script
*/

function onOpen() {

  // add a custom menu to the spreadsheet
  SpreadsheetApp.getUi()
    .createMenu('Admin')
    .addItem('Get Files', 'getFiles') // label for menu item, name of function to run.
    .addToUi();

}