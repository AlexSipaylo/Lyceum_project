import React from 'react'
import { useNavigate } from 'react-router-dom'
import avatarPath from '../../images/chatAvatar.png'

const ChatItem = ({ chat, isUserChat }) => {
    const navigate = useNavigate()

    const handleJoinClick = () => {
        navigate(`/chat?name=${chat.name}`)
    }

    const lastMessage = 
        chat.data.length > 0 ?
            chat.data[chat.data.length - 1].text ?
                chat.data[chat.data.length - 1].text :
                'Вложенные файлы...' :
        'Сообщений пока нет...'

    return (
        <div className="d-flex flex-column flex-sm-row align-items-start align-items-sm-center justify-content-between p-2 border-bottom" onClick={handleJoinClick} style={{ cursor: 'pointer' }}>
            <div className='d-flex'>
                <img src={avatarPath} alt="Avatar" className="rounded-circle me-3" style={{ width: '50px', height: '50px' }} />
                <div className="flex-grow-1">
                    <h5 className="text mt-0">{chat.name}</h5>
                    <p className="text-muted text">{lastMessage}</p>
                </div>
            </div>
            {!isUserChat &&
            (
                <button className="btn btn-primary align-self-end align-self-sm-center" onClick={handleJoinClick}>
                    Присоединиться
                </button>
            )}
        </div>
    )
}

export default ChatItem
