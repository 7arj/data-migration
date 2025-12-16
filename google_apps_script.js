function onEdit(e) {
  var range = e.range;
  var sheet = range.getSheet();
  
  // Column 2 is Email. If user edits an email, validate it.
  if (range.getColumn() == 2) { 
    var email = range.getValue().toString();
    var statusCell = range.offset(0, 3); // Moves 3 columns right (to Column E)
    
    // Strict Regex for Email Validation
    // 1. Must start with characters (no special chars like @ at start)
    // 2. Must have an @ symbol in the middle
    // 3. Must have a domain name after @
    // 4. Must end with a dot and 2-6 letters (e.g., .com, .co.in)
    var emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    
    if (emailPattern.test(email)) {
      statusCell.setValue(" Ready for ETL");
      statusCell.setFontColor("green");
      statusCell.setBackground("#e6fffa");
    } else {
      statusCell.setValue(" Invalid Email");
      statusCell.setFontColor("red");
      statusCell.setBackground("#ffe6e6");
    }
  }
}