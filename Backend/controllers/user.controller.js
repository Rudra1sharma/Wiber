import User from "../Models/user.model.js";

export const getUsersForSidebar = async (req, res) => {
    try {
        const loggedInUserId = req.user._id;

        // find every user in our db but the one that is not equal to user id
        // if you want to send message to yourself than remove this->{ _id: { $ne: loggedInUserId }}
        
        // for wanting send message to yourself code will be :-
 // ->  const filteredUsers = await User.find().select("-password");
        
        // for not sending message to ourself :- 
        
        const filteredUsers = await User.find({ _id: { $ne: loggedInUserId } }).select("-password");

		res.status(200).json(filteredUsers);
        
    } catch (error) {
        console.error("error in getUsersForSidebar: ", error.message);
        res.status(500).json({ error: "Internal Server Error" });
    }
}