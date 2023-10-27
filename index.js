const express = require('express');
const multer = require('multer');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');
const app = express();
app.use(cors());
const port = process.env.PORT || 3000;

// Multer configuration for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/'); // Store uploaded files in the 'uploads' directory
  },
  filename: function (req, file, cb) {
    console.log(req);
    cb(null, Date.now() + '-' + file.originalname); // Rename files to avoid conflicts
  },
});
const upload = multer({ storage: storage });

// Body parser setup
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb+srv://greatedafeoke:nVtAQ8fgT3981URz@cluster0.rfzp39w.mongodb.net/server?retryWrites=true&w=majority', { useNewUrlParser: true });

// Define a Mongoose model for image documents
const Image = mongoose.model('Image', {
  filename: String,
  date: String,
  latitude: String,
  longitude: String,
  publicUrl: String,
});

// API endpoint for uploading images
app.post('/upload', upload.single('image'), async (req, res) => {
  const file = req.file;
  const { date, latitude, longitude, publicUrl } = req.body; // You can send additional data with the request
  if (!file) {
    return res.status(400).json({ error: 'No file uploaded.' });
  }
  
  console.log(req.body);
  // console.log(req);
  // Save image information to the MongoDB database
  const image = new Image({
    filename: file.filename,
    date: date || new Date().toISOString(),
    latitude: latitude || 0,
    longitude: longitude || 0,
    publicUrl: publicUrl || "",
  });

  try {
    await image.save();
    return res.json({ message: 'Image uploaded and information saved.' });
  } catch (err) {
    return res.status(500).json({ error: 'Error saving image information.' + err.message });
  }
});

// API endpoint to retrieve image information
app.get('/images', async (req, res) => {
  try {
    const images = await Image.find({});
    return res.json(images);
  } catch (err) {
    return res.status(500).json({ error: 'Error retrieving images.' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
