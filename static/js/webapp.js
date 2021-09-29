Dropzone.autoDiscover = false;
var myDropzone = new Dropzone('#my-awesome-dropzone', {       
    paramName: "file", 
    maxFilesize: 3.0, 
    maxFiles: 4,
    parallelUploads: 10000,
    dictDefaultMessage: "Drag file 70A_人_Webアプリ(MCHC社向け)_20210901 or 70B_所属_Webアプリ(MCHC社向け)_20210806",
    acceptedFiles : ".csv",
    uploadMultiple: true,
    autoProcessQueue: false,
    init: function() {
    	$("#loading").removeAttr("hidden")
		$("#loading").hide();
		var myDropzone = this;  
		$(document).on("click", '#btn-upload-file', function(event){
			 $("#loading").show();
			 event.preventDefault();
			 myDropzone.processQueue();
		 });
		  this.on('successmultiple', function(file, response) {
			  console.log(response)
			  
			  setTimeout(function(){ 
				   rows = response.split("\n");
				   filename="70A_人_Webアプリ(MCHC社向け)_20210901_converted.csv"
				    var csvFile = '';
				    for (var i = 0; i < rows.length; i++) {
				        csvFile += rows[i];
				    }
				    var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
				    if (navigator.msSaveBlob) { // IE 10+
				        navigator.msSaveBlob(blob, filename);
				    } else {
				        var link = document.createElement("a");
				        if (link.download !== undefined) { // feature detection
				            // Browsers that support HTML5 download attribute
				            var url = URL.createObjectURL(blob);
				            link.setAttribute("href", url);
				            link.setAttribute("download", filename);
				            link.style.visibility = 'hidden';
				            document.body.appendChild(link);
				            link.click();
				            document.body.removeChild(link);
				        }
				    }
				    $("#loading").hide();
				    myDropzone.removeAllFiles();  
			  }, 3000);
	        });
    }


    
});
