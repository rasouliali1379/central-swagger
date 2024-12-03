import React, {useState} from "react";
import {Box, Button, Paper, TextField, Typography,} from "@mui/material";
import {useNavigate} from "react-router-dom"; // For navigation
import axios from "axios";

const LoginAndTable = () => {
    const [secret, setSecret] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();


    const handleLogin = async () => {
        try {
            const response = await axios.get(process.env.REACT_APP_API_LIST_URL + "/all", {headers: {'x-secret': secret}});

            localStorage.setItem("adminSecret", secret);
            if (response.status === 200) {
                navigate("/services", {state: {items: response.data.items || []}});
            } else {
                setError("Login failed. Please check the secret.");
            }
        } catch (err) {
            setError("An error occurred during login.");
        }
    };

    return (
        <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
            minHeight="100vh"
            bgcolor="#f5f5f5"
            padding={3}
        >
            <Paper elevation={3} sx={{padding: 4, width: 300}}>
                <Typography variant="h6" align="center" marginBottom={2}>
                    Admin Login
                </Typography>
                <TextField
                    label="Admin Secret"
                    type="password"
                    fullWidth
                    variant="outlined"
                    value={secret}
                    onChange={(e) => setSecret(e.target.value)}
                    margin="normal"
                />
                {error && (
                    <Typography variant="body2" color="error" align="center" marginBottom={2}>
                        {error}
                    </Typography>
                )}
                <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    onClick={handleLogin}
                >
                    Login
                </Button>
            </Paper>
        </Box>
    );
};

export default LoginAndTable;