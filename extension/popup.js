document.addEventListener('DOMContentLoaded', function() {
  var selectedText = '';
  var click=false; 
  chrome.tabs.executeScript({
    code: "window.getSelection().toString();"
  }, function(selection) {
    selectedText = selection[0];
    document.getElementById('selectedText').innerText = selectedText;
  });

  document.getElementById('summarizeBtn').addEventListener('click', function() {
    if (selectedText !== '') {
      document.getElementById('summaryLengthSlider').addEventListener('click', function() {
        var sliderValue = document.getElementById('summaryLengthSlider').value;
        document.getElementById('sliderValue').innerText = " "+ sliderValue+"%"; 
        if (selectedText !== '') {
          summarizeText(selectedText);
        } else {
          alert('No text selected!');
        }
      });
      click=true;
      summarizeText(selectedText);
      document.getElementById('selectedText').style.display = 'block'; // Hide selected text
      document.getElementById('summary').style.display = 'block';
      document.getElementById('keywords').style.display = 'block'; // Show summary
    } else {
      alert('No text selected!');
    }
  });

  function summarizeText(text) {
    var sliderValue = document.getElementById('summaryLengthSlider').value;
    fetch('http://127.0.0.1:5003/summary', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: text,
        sliderValue: sliderValue
      })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('summary').innerText = "Summary: " + data.summary;
      document.getElementById('keywords').innerText = "Keywords: " + data.keywords.join(" , ");
    })
    .catch(error => console.error('Error:', error));
  }
});
document.getElementById('summaryLengthSlider').addEventListener('click', function()
{
    var sliderValue = document.getElementById('summaryLengthSlider').value;
    document.getElementById('sliderValue').innerText = " "+ sliderValue+"%"; 
    
});