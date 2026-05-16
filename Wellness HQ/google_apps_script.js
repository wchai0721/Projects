// ═══════════════════════════════════════════════════════════
//  Wen's Wellness Dashboard — Google Apps Script
//  Paste this entire file into Google Apps Script editor
//  Then deploy as a Web App (see setup_guide.txt for steps)
// ═══════════════════════════════════════════════════════════

const SHEET_NAME = "Wellness Log";
const RECOVERY_SHEET = "Recovery Log";
const NOTES_SHEET = "Session Notes";

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    if (data.action === 'sync') {
      writeSync(data);
    }
    return ContentService
      .createTextOutput(JSON.stringify({status:'ok'}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch(err) {
    return ContentService
      .createTextOutput(JSON.stringify({status:'error', message: err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({status:'ok', message:'Wen Wellness Script is live'}))
    .setMimeType(ContentService.MimeType.JSON);
}

function writeSync(data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();

  // ── 1. Weekly Progress sheet ──────────────────────────────
  let progressSheet = ss.getSheetByName(SHEET_NAME);
  if (!progressSheet) {
    progressSheet = ss.insertSheet(SHEET_NAME);
    progressSheet.appendRow([
      'Timestamp', 'Date',
      'Workouts', 'Streak', 'Classes', 'Walking',
      'Strength workouts', 'Pilates class', 'Walking days', 'Mobility sessions', 'Movement snacks'
    ]);
    progressSheet.getRange(1,1,1,11).setFontWeight('bold').setBackground('#E1F5EE');
    progressSheet.setFrozenRows(1);
  }

  const metrics = data.metrics || {};
  const targets = data.targets || [];
  const targetVals = targets.map(t => t.cur + '/' + t.max);

  progressSheet.appendRow([
    data.timestamp,
    data.date,
    metrics.workouts || '',
    metrics.streak || '',
    metrics.classes || '',
    metrics.walking || '',
    targetVals[0] || '',
    targetVals[1] || '',
    targetVals[2] || '',
    targetVals[3] || '',
    targetVals[4] || '',
  ]);

  // ── 2. Recovery Log sheet ────────────────────────────────
  let recoverySheet = ss.getSheetByName(RECOVERY_SHEET);
  if (!recoverySheet) {
    recoverySheet = ss.insertSheet(RECOVERY_SHEET);
    recoverySheet.appendRow([
      'Timestamp', 'Date', 'Sleep', 'Hydration', 'Steps', 'Energy', 'Mobility', 'Stress', 'Notes'
    ]);
    recoverySheet.getRange(1,1,1,9).setFontWeight('bold').setBackground('#EEEDFE');
    recoverySheet.setFrozenRows(1);
  }

  const rec = data.recovery || {};
  recoverySheet.appendRow([
    data.timestamp,
    data.date,
    rec.sleep || '',
    rec.hydration || '',
    rec.steps || '',
    rec.energy || '',
    rec.mobility || '',
    rec.stress || '',
    (data.notes && data.notes.recovery) ? data.notes.recovery : ''
  ]);

  // ── 3. Session Notes sheet ───────────────────────────────
  let notesSheet = ss.getSheetByName(NOTES_SHEET);
  if (!notesSheet) {
    notesSheet = ss.insertSheet(NOTES_SHEET);
    notesSheet.appendRow(['Timestamp', 'Date', 'Day', 'Note']);
    notesSheet.getRange(1,1,1,4).setFontWeight('bold').setBackground('#FAEEDA');
    notesSheet.setFrozenRows(1);
  }

  if (data.notes && data.notes.workout) {
    data.notes.workout.forEach(entry => {
      if (entry.note && entry.note.trim()) {
        notesSheet.appendRow([data.timestamp, data.date, entry.day, entry.note]);
      }
    });
  }

  // ── 4. Auto-resize all columns ───────────────────────────
  [progressSheet, recoverySheet, notesSheet].forEach(sheet => {
    sheet.autoResizeColumns(1, sheet.getLastColumn());
  });
}
