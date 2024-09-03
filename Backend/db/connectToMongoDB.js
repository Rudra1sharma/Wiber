import mongoose from "mongoose";
import dotenv from 'dotenv'
dotenv.config();


const connectToMongoDB = async () => {
	try {
		await mongoose.connect(process.env.MONGO_DB_URI);
		console.log("Database Connected...");
	} catch (error) {
		console.log("Error connecting to Database", error.message);
	}
};

export default connectToMongoDB;				