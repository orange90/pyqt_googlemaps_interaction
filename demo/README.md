# pyqt_googlemaps_interaction sample
a sample introduce how to integrate google maps into pyqt.
But first you need to apply for an api key in google first.
https://developers.google.com/maps/documentation/javascript/get-api-key
go to this link to apply for your key and put in in  'map.html', search map.html for "YOUR_KEY_HERE", then replace it with the key you just applied.
## Feature can be refered to:
* create web view in pyqt(javascript will be executed here)
* read file
* create javascript command
* execute js command
* create file
* save file

## Advantage 
* easy debug. Html file and python files are seperated, you can debug you webpage using Chrome console first, and then debug in your python code.

## How python interact with webview
1. create web view 
```python
self.view  = QtWebKit.QWebView()
```
2. get frame in web view
```python
frame = self.view.page().mainFrame()
```
3. pass script to web view
```python
script = "loadData(%s)"%lines
returnvalue = frame.evaluateJavaScript(script)
```

