import React, { useState, useEffect } from 'react';
import "./App.css";
import io from 'socket.io-client';
import ProgressBar from "@ramonak/react-progress-bar";
import Navbar from './Navbar';


const socket = io.connect('http://127.0.0.1:5000');

const Folder = () => {
    const [error, setError] = useState(null);
    const [newfilecount, setnewfilecount] = useState(0);
    const [oldfilecount, setoldfilecount] = useState(0);
    const [currentCount, setCurrentCount] = useState(0);
    const [dublicateCount, setdublicateCount] = useState(0);
    const [noEmail, setnoEmail] = useState(0)
    const [totalCount, setTotalCount] = useState(0);
    const [no_files, setno_files] = useState(0);
    const [seletedfile, setseletedfile] = useState(null)
    const [progress, setprogress] = useState(0)
    const [pdffiles, setpdffiles] = useState(0)
    const [docxfiles, setdocxfiles] = useState(0)
    const [docfiles, setdocfiles] = useState(0)
    const [rtffiles, setrtffiles] = useState(0)
    const [txtfiles, settxtfiles] = useState(0)
    const [details, setDetails] = useState("")
    const [dataArray, setDataArray] = useState([]);
    const [result, setResult] = useState("")
    const [showDate, setshowDate] = useState(true)
    const [date, setDate] = useState("")

    useEffect(() => {
        let a = 0;
        socket.on('progress_update', data => {
            setCurrentCount(data.current_count);
            setTotalCount(data.total_count);
            setnewfilecount(data.new_count);
            setoldfilecount(data.old_count);
            setdublicateCount(data.dublicate_count)
            setnoEmail(data.none_email)
            setprogress(Math.round((data.current_count / data.total_count) * 100))
        });
        socket.on('parse_complete', data => {
            // Handle completion if needed
        });

        return () => {
            socket.off('progress_update');
            socket.off('parse_complete');
        };
    }, [currentCount, totalCount]);

    const handleParseResume = async (e) => {
        e.preventDefault();

        try {
            const resumeFileInput = document.getElementById('resumeFile');
            const resumeFiles = resumeFileInput.files;
            setno_files(resumeFiles.length);

            const formData = new FormData();
            for (let i = 0; i < resumeFiles.length; i++) {
                formData.append('resumes[]', resumeFiles[i]);
            }
            formData.append('isFolderUpload', true);

            const response = await fetch('http://127.0.0.1:5000/resumeparse', {
                method: 'POST',
                body: formData,
                mode: 'cors',
            });

            if (response.ok) {

            } else {
                setError('Failed to parse resume');
            }
        } catch (error) {
            console.error('Error parsing resume:', error);
            setError('An error occurred while parsing the resume');
        }
    };

    const handlechange = (e) => {
        const files = e.target.files;
        setseletedfile(files)
        const pdfFiles = Array.from(files).filter(file => file.type === 'application/pdf');
        const numberOfPdfFiles = pdfFiles.length;
        setpdffiles(numberOfPdfFiles)
        const docxfiles = Array.from(files).filter(file => file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
        const numberOfdocxFiles = docxfiles.length;
        setdocxfiles(numberOfdocxFiles)
        const docfiles = Array.from(files).filter(file => file.type === 'application/msword');
        const numberOfdocFiles = docfiles.length;
        setdocfiles(numberOfdocFiles)
        const rtffiles = Array.from(files).filter(file => file.type === 'application/rtf');
        const numberOfrtfFiles = rtffiles.length;
        setrtffiles(numberOfrtfFiles)
        const txtfiles = Array.from(files).filter(file => file.type === 'text/plain');
        const numberOftxtFiles = txtfiles.length;
        settxtfiles(numberOftxtFiles)

    }
    const handleClick = async (date, accept) => {
        console.log(accept);
        const dateTime = date || "";
        const data = {
            accept: accept,
            date: dateTime
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/accept', {
                method: 'POST',
                body: JSON.stringify(data),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const value = await response.json();

                let input = JSON.parse(value.res);
                console.log(input.result)
                if (input.result === 'changable') {
                    setshowDate(false)
                }
                else {
                    alert(`You have already ${input.result}ed the value`)
                    console.log(input.result)
                    setshowDate(true)
                }
                setResult(value.res)
            } else {
                throw new Error('Network response was not ok');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };
    const handleold = async () => {
        try {
            setprogress(0)
            const response = await fetch('http://127.0.0.1:5000/previous', {
                method: 'POST',
                mode: 'cors',
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }
            const data = await response.json();
            console.log(data);
            const newDataArray = Object.entries(data).map(([key, value]) => ({ key, value }));
            setDataArray(newDataArray);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleDate = async (date) => {
        try {
            const response = await fetch('http://127.0.0.1:5000/date', {
                method: 'POST',
                body: date,
                mode: 'cors',
            });

            if (!response.ok) {
                throw new Error('Failed to fetch data');
            }

            const data = await response.json(); // Wait for the JSON data
            setnewfilecount(data.newfile)
            setoldfilecount(data.oldfile)
            setdublicateCount(data.duplicatefile)
            setnoEmail(data.noEmail)
            setDate(date)
            handleClick(date, "")



        } catch (error) {
            console.error('Error:', error);
        }
        console.log(date)
    };


    return (
        <div>
            <div>
                <Navbar />
            </div>
            <div className='main-div-bottom'>
                <div className='main-page'>
                    <div className='old-data'>
                        <div>
                            <button className="old-bttn" onClick={() => handleold()}>previous Data</button>
                        </div>
                        <div>
                            {dataArray.map((item, index) => (
                                <div key={index}>

                                    <p className='date' onClick={() => handleDate(item.value)}>
                                        {item.value}
                                    </p>

                                </div>
                            ))}
                        </div>
                    </div>
                    <div className='new-data'>
                        <div className='upload-main-div'>
                            <div className='upload-resume'>
                                <div>
                                    <div>
                                        <img src='https://truetalent.io/Assets/svgs/upload.svg' className='img-upload' />
                                        <input type="file" id="resumeFile" name="files[]" accept=".pdf,.doc,.docx,.rtf,.txt" directory="" webkitdirectory="" onChange={handlechange} multiple required
                                            style={{ color: seletedfile ? "#14BC9A" : "white" }} className='choose-bttn'>
                                        </input>

                                    </div>

                                </div>
                            </div>
                            <div className='upload-buut-div'>
                                <button type="submit" className='upload-button' onClick={handleParseResume}>Parse Folder</button>
                            </div>

                        </div>
                        <div>
                            <div className='tot-div'>

                                {no_files == 0 ? <div></div> : <div className='para-div'>
                                    <p className='para-txt para-text'>(pdf files: {pdffiles}</p>
                                    <p className='para-txt'>doc files: {docfiles}</p>
                                    <p className='para-txt'>docx files: {docxfiles}</p>
                                    <p className='para-txt'>Rtf files: {rtffiles}</p>
                                    <p className='para-txt'>txt files: {txtfiles})</p>
                                </div>}
                            </div>
                            <div>
                                {no_files == 0 ? <div></div> :
                                    <div>
                                        <ProgressBar completed={progress}
                                            baseBgColor='#efcfcf'
                                            bgColor='#14BC9A'
                                            height='10px'
                                            width='48.5%'
                                            labelSize="9px"
                                        />
                                    </div>

                                }
                            </div>
                            <div>
                                <div>
                                    <form className='count-value'>
                                        <div className='count-value-main'>
                                            <div className='count-value-div'>
                                                <div className='count-value-input'>
                                                    <label className='font-size'>Total files Uploaded: </label> <br />
                                                    <input value={no_files} className='input-value'></input>
                                                </div>
                                                <div className='count-value-input'>
                                                    <label className='font-size'>Unique files:</label> <br />
                                                    <input value={newfilecount} className='input-value'></input>
                                                </div>
                                                <div className='count-value-input'>
                                                    <label className='font-size'>Dublicate files in this batch: </label> <br />
                                                    <input value={dublicateCount} className='input-value'></input>
                                                </div>

                                            </div>
                                            <div className='count-value-div'>
                                                <div className='count-value-input1'>
                                                    <label className='font-size'>Files without Email: </label> <br />
                                                    <input value={noEmail} className='input-value'></input>
                                                </div>
                                                <div className='count-value-input1'>
                                                    <label className='font-size'>Pre-Exsisting files in TT-Database: </label> <br />
                                                    <input value={oldfilecount} className='input-value'></input>
                                                </div>
                                                
                                                    
                                                        {
                                                            progress == 100 ?
                                                                <div className='count-value-input1'>
                                                                    <label className='font-size'>TT Cash eligiblity: </label> <br />
                                                                    <input value={newfilecount * 5} className='input-value'></input>
                                                                </div>
                                                                : ""
                                                        }
                                                    
                                                
                                                <div>
                                                    
                                                </div>

                                            </div>
                                        </div>
                                    </form>
                                </div>

                            </div>
                            <div>
                                {
                                    progress == 100 ?
                                        <div className='tt-bbtn'>
                                            <button className="tt-decline-btn" onClick={() => handleClick("", "Accept")}>Accept</button>
                                            <button className="tt-accept-btn" onClick={() => handleClick("", "Decline", "")}>Decline</button>

                                        </div>
                                        : ""
                                }
                                {
                                    showDate == true ? "" : <div className='tt-bbtn'>
                                        <button className="tt-decline-btn" onClick={() => handleClick(date, "Accept")}>Accept</button>
                                        <button className="tt-accept-btn" onClick={() => handleClick(date, "Decline")}>Decline</button>
                                    </div>
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default Folder