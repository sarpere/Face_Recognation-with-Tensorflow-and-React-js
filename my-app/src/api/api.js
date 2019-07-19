import axios from 'axios';
axios.defaults.baseURL = 'http://127.0.0.1:5002';


export async function GetStudents() {
    const res = await axios.get(`/students`)
    return res.data.data;
}

export async function SavePhoto(photo) {
    const res = await axios.post(`/rollcall`,  photo );
    return res.data;
  }
export async function AddNewStudent(Name,schoolNumber, images){
    var newStudent ={'Name': Name, 'schoolNumber':schoolNumber,'images':images}
    var res =  await axios.post(`/AddNewStudent`,  newStudent )
    return true
}