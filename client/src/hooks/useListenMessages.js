import { useEffect } from "react";

import { useSocketContext } from "../context/SocketContext";
import useConversation from "../zustand/useConversation";


const useListenMessages = () => {
	const { socket } = useSocketContext();
	const { messages, setMessages } = useConversation();
	useEffect(() => {
		const handleNewMessage = (newMessage) => {
			newMessage.shouldShake = true;
			console.log("chlja");
			console.log(newMessage);
        	setMessages(prevMessages => [...prevMessages, newMessage]);
    	};
		
		socket?.on("newMessage", handleNewMessage);

		return () => socket?.off("newMessage", handleNewMessage);
	}, [messages,socket]);
};
export default useListenMessages;