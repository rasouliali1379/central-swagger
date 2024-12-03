import React, {useEffect, useState} from "react";
import {
    Box,
    Button,
    Checkbox,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    IconButton,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography
} from "@mui/material";
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import axios from "axios";
import {useLocation, useNavigate} from "react-router-dom";

const Services = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [items, setItems] = useState(location.state?.items || []);
    const [adminSecret] = useState(localStorage.getItem("adminSecret") || "");
    const [openAddDialog, setOpenAddDialog] = useState(false);
    const [openResultDialog, setOpenResultDialog] = useState(false);
    const [newService, setNewService] = useState({name: "", exposed: false});
    const [createdService, setCreatedService] = useState(null);

    useEffect(() => {
        if (!adminSecret) {
            navigate("/admin");
        }
    }, [adminSecret, navigate]);

    const refreshItems = async () => {
        try {
            const response = await axios.get(process.env.REACT_APP_API_LIST_URL + "/all", {headers: {'x-secret': adminSecret}});
            setItems(response.data.items);
        } catch (err) {
            console.error("Failed to refresh services:", err);
        }
    };

    const handleAddService = async () => {
        try {
            console.log(adminSecret)
            const response = await axios.post(
                process.env.REACT_APP_API_LIST_URL,
                {...newService},
                {headers: {'x-secret': adminSecret}});
            setCreatedService(response.data);
            setOpenResultDialog(true);
        } catch (err) {
            console.error("Failed to create service:", err);
        } finally {
            setOpenAddDialog(false);
        }
    };

    const handleCopy = (text) => {
        navigator.clipboard.writeText(text);
    };

    const closeResultDialog = () => {
        setOpenResultDialog(false);
        refreshItems();
    };

    return (
        <Box width="80%" margin="auto" padding={3}>
            <Typography variant="h5" gutterBottom>
                Items
            </Typography>
            <Button
                variant="contained"
                color="primary"
                onClick={() => setOpenAddDialog(true)}
                sx={{marginBottom: 2}}
            >
                Add Service
            </Button>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Key</TableCell>
                            <TableCell>Name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {items.map((item) => (
                            <TableRow key={item.key}>
                                <TableCell>{item.key}</TableCell>
                                <TableCell>{item.name}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Add Service Dialog */}
            <Dialog open={openAddDialog} onClose={() => setOpenAddDialog(false)}>
                <DialogTitle>Add New Service</DialogTitle>
                <DialogContent>
                    <TextField
                        label="Service Name"
                        fullWidth
                        margin="normal"
                        value={newService.name}
                        onChange={(e) =>
                            setNewService({...newService, name: e.target.value})
                        }
                    />
                    <Box display="flex" alignItems="center" marginTop={2}>
                        <Checkbox
                            checked={newService.exposed}
                            onChange={(e) =>
                                setNewService({...newService, exposed: e.target.checked})
                            }
                        />
                        <Typography>Exposed</Typography>
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenAddDialog(false)}>Cancel</Button>
                    <Button variant="contained" onClick={handleAddService}>
                        Add
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Result Dialog */}
            <Dialog open={openResultDialog} onClose={closeResultDialog}>
                <DialogTitle>Service Created</DialogTitle>
                <DialogContent>
                    {createdService && (
                        <>
                            <Box display="flex" alignItems="center" marginBottom={2}>
                                <Typography variant="body1" sx={{flexGrow: 1}}>
                                    Key: {createdService.key}
                                </Typography>
                                <IconButton onClick={() => handleCopy(createdService.key)}>
                                    <ContentCopyIcon/>
                                </IconButton>
                            </Box>
                            <Box display="flex" alignItems="center">
                                <Typography variant="body1" sx={{flexGrow: 1}}>
                                    Secret: {createdService.secret}
                                </Typography>
                                <IconButton onClick={() => handleCopy(createdService.secret)}>
                                    <ContentCopyIcon/>
                                </IconButton>
                            </Box>
                        </>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={closeResultDialog}>Close</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default Services;