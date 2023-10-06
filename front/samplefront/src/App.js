import logo from './logo.svg';
import './App.css';
import {useEffect, useState} from "react";
import {parseCookies, setCookie} from 'nookies';
import axios, {all} from "axios";

function App() {
    const [isLogin, setIsLogin] = useState(false)
    const [username, setUsername] = useState()
    const [password, setPassword] = useState()

    const cookies = parseCookies();


    function SampleReq() {
        const accessToken = cookies.access_token;

        axios({
            url: "http://localhost:4000/",
            method: "GET",
            headers: {"Auth": accessToken},


        }).then(resp => {
            alert("[+] Sample req was sent to localhost:4000")
        }).catch(err => {
            console.log(err)
            alert("[-] Request was not sent")
        })
    }


    function isLoginHandler() {
        const accessToken = cookies.access_token;
        if (accessToken == undefined) {
            setIsLogin(false)
            return false
        } else {
            axios({
                url: "http://localhost:8000/accounts/verify/",
                data: {"token": accessToken},
                method: "POST"
            }).then(resp => {
                setIsLogin(true)
                return true
            }).catch(err => {
                setIsLogin(false)
                return false
            })


        }


    }


    function loginHandler() {
        axios({
            method: "POST", url: "http://localhost:8000/accounts/token/", data: {"phone": username, "code": password}
        }).then(resp => {
            console.log(resp.data.token)
            setCookie(null, 'access_token', resp.data.token, {
                maxAge: 30 * 24 * 60 * 60, // 30 days
                path: '/', domain: '.domain.com',
            });
            alert("Login successsd")
            setIsLogin(true)
        }).catch(err => {
            alert("Login is not correct")
        })

    }

    useEffect(() => {
        isLoginHandler()
    }, []);


    return (<div className="App">
        <header className="App-header">
            <img src={logo} className="App-logo" alt="logo"/>
            <p>
                Welcome to mehras dreams sso system

            </p>
            {isLogin ?

                <div>
                    <h1>You are login</h1>
                    <h1><a onClick={SampleReq}>Sample req</a></h1>
                </div>
                : <div>
                    <h1>You are not login</h1>
                    <h2>Login to my system</h2>

                    <input type="text" placeholder={"Username"}
                           onChange={event => setUsername(event.target.value)}></input>
                    <br/>
                    <input type="password" placeholder={"Password"}
                           onChange={event => setPassword(event.target.value)}></input>
                    <br/>
                    <button onClick={loginHandler}>Login now</button>
                </div>


            }
            <a
                className="App-link"
                href="https://reactjs.org"
                target="_blank"
                rel="noopener noreferrer"
            >
                Learn React
            </a>
        </header>
    </div>);
}

export default App;
