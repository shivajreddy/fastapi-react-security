// :: LOGIN PAGE
import { useEffect, useRef, useState } from "react"
import { useNavigate } from "react-router-dom";
import { useLoginMutation } from "./authApiSlice";
import { useAppDispatch } from "@/hooks/hooks";
import { setAuthState } from "./authSlice";


function LoginPage() {

  const userRef = useRef();
  const errRef = useRef();
  const [username, setUsername] = useState('');
  const [errMessage, setErrMessage] = useState('');
  const [plainPwd, setPlainPwd] = useState('');

  const navigate = useNavigate();

  const [login, { isLoading }] = useLoginMutation();
  const dispatch = useAppDispatch();

  useEffect(() => {
    userRef.current.focus();
  }, [])

  useEffect(() => {
    setErrMessage('')
  }, [username, plainPwd])

  async function handleFormSubmission(e) {
    e.preventDefault();
    try {
      const userData = await login({ username: username, plainPassword: plainPwd }).unwrap();
      dispatch(setAuthState({ user: userData, accessToken: '' }))
      setUsername(''); setPlainPwd('');
    } catch (error) {
      console.error("Error:", error)
    }
  }

  return (
    <div>Login</div>
  )
}



export default LoginPage