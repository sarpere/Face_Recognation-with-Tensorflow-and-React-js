import React, { Component } from 'react';
import Webcam from "react-webcam";
import ReactTable from 'react-table'
import 'react-table/react-table.css'
import tik from '../tik.png'
import { SavePhoto, GetStudents } from '../api/api'
class WebcamCapture extends Component {
  constructor(state) {
    super(state)
    this.bool = null
    this.state = {
      persons: [],
      data: [],
      studentData: []
    }
  }

  componentDidMount() {
    this.getStudents();
  }
  getStudents = () =>{
    GetStudents().then((d) => {
      this.setState({
        data: d
      })
      this.props.NewStudentAdd(false);
    });

  }
  setRef = webcam => {
    this.webcam = webcam;
  };
  componentDidUpdate(){
    if(this.props.addedNewStudent){
      this.getStudents();
      console.log(this.state.data)

    }
  }
  capture = () => {
    const canvas = this.refs.canvas
    const ctx = canvas.getContext("2d")
    var studentsIn = []
    SavePhoto(this.webcam.getScreenshot()).then(res => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      ctx.beginPath();
      ctx.font = "bold 20px Courier"
      var data = res
      data.map(x => {
        x.here = "true";
        var Name = ""
        var unknown = "Unknown"
        this.state.data.map(k => {

          if (x.id === k.id) {
            Name = k.Name
            studentsIn.push(k)
          }
          if (x.id === -1) {
            Name = unknown

          }
        })
        ctx.fillText(Name, x.bb0 - 30, x.bb1 - 40)
        ctx.rect((x.bb0/1.12), (x.bb1/0.97) - 30, x.bb2 - x.bb0, x.bb3 - x.bb1);
        ctx.stroke()
        studentsIn.map(k => {
          var bool = true
          this.state.studentData.map(x => {
            if (x.id === k.id)
              bool = false
          })
          if (bool)
            this.setState(prevState => ({
              studentData: [...prevState.studentData, k]
            }))

        })


      })
      return this.capture()
    })


  };

  render() {
    const videoConstraints = {
      width: 1280,
      height: 720,
      facingMode: "user"
    };
    const columns = [{
      Header: 'İsim - Soyisim',
      accessor: 'Name'
    }, {
      Header: 'Okul Numarası',
      accessor: 'Schoolno'
    }, {
      Header: 'Dosya Id',
      accessor: 'FileId'

    }, {
      Header: 'yoklama',
      accessor: 'here',
      Cell: row => (
        <div
          style={{
            width: '100%',
            height: '100%',
            textAlign: "center"
          }}
        >
          <img src={tik} alt="here" width="20" height="20" />
        </div>
      )
    }
    ]
    return (
      <div className="top">
        <div className="Students">
          {this.state.data &&
            <ReactTable
              data={this.state.studentData}
              showPageSizeOptions={false}
              columns={columns}
              className="Table"
              defaultPageSize={6}
            />}
        </div>
        <div className="Students" style={{ float: "right" }}>
          <Webcam
            audio={false}
            height={280}
            ref={this.setRef}
            screenshotFormat="image/jpeg"
            width={550}
            videoConstraints={videoConstraints}
            className="Cam"
          />
          <canvas ref="canvas" width={530} height={300} />
          <button className="button" onClick={this.capture}>Fotoğraf Çek</button>
        </div>
      </div>
    );
  }

}

export default WebcamCapture;