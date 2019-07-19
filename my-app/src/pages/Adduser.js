// @flow strict

import * as React from 'react';
import {AddNewStudent} from '../api/api.js'
class Adduser extends React.Component {
    constructor(state) {
        super(state)
        this.state = {
            imageFiles: []
        }
    }
    
    filesHandler = (event) => {
        
        var files = event.target.files; // FileList object
        var images_Array=[]
        // Loop through the FileList and render image files as thumbnails.
        for (var i = 0, f; f = files[i]; i++) {
    
            // Only process image files.
            if (!f.type.match('image.*')) {
                continue;
            }
    
            var reader = new FileReader();
    
            // Closure to capture the file information.
            reader.onload = (function (theFile) {
                return function (e) {
                    // Render thumbnail.
                    images_Array.push(e.target.result.split(',')[1])

                };
            })(f);
    
            // Read in the image file as a data URL.
            reader.readAsDataURL(f);
        }
       this.setState({imageFiles:images_Array})
    }
    submitHandler = () => {
        const parentList = document.getElementById('Container');
        const ListChild = parentList.children;
        var Name = ListChild[0].value
        var schoolNumber = ListChild[1].value
        AddNewStudent(Name,schoolNumber,this.state.imageFiles)
        this.props.NewStudentAdd(true);
    }
    render() {
        return (
            <div id="Adduser">
                <div id="Container">
                    <input type="text" placeholder="İsim giriniz.." />
                    <input type="text" placeholder="Okul numaranız giriniz.." />
                    <input type="file" id="file" multiple onChange={this.filesHandler} />
                    <button onClick={this.submitHandler}> Yeni öğrenci Ekle</button>
                </div>
            </div>
        );
    }
}

export default Adduser;