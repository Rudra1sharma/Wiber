import { useState } from "react";
import useConversation from "../zustand/useConversation";
import toast from "react-hot-toast";

const useSendMessage = () => {
	const [loading, setLoading] = useState(false);
	const { messages, setMessages, selectedConversation } = useConversation();

	const sendMessage = async (message) => {
		setLoading(true);
		try {
			let encMessage = message + " dummy";
			console.log("Encoded 1: " + encMessage)
			// console.log(encMessage);
			const res = await fetch(`/api/messages/send/${selectedConversation._id}`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ message, encMessage}),
			});
			const data = await res.json();
			if (data.error) throw new Error(data.error);
			// data = [...data, "Loda lelo mera"];

			// data.message += " Lund lele mera sahil";
			console.log("Printed Message: " + data.message);
			
			setMessages([...messages, data]);
		} catch (error) {
			toast.error(error.message);
		} finally {
			setLoading(false);
		}
	};

	return { sendMessage, loading };
};
export default useSendMessage;