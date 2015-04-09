

proc getResult {model_file}  {
	hwi GetSessionHandle ses1
	ses1 GetProjectHandle pro1
	pro1 GetPageHandle page1 1
	page1 GetWindowHandle win1 1
	win1 SetClientType Animation
	win1 GetClientHandle cli
	cli AddModel $model_file
	ses1 CaptureScreen png test.png 
	ses1 Close
}

getResult @filename@
catch {destroy .}
