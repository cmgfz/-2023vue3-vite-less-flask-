export default function formatDate(datetime) {
    let date = new Date(datetime); //datetime时间戳为13位毫秒级别,如为10位需乘1000
    let month = ("0" + (date.getMonth() + 1)).slice(-2)
    let sdate = ("0" + date.getDate()).slice(-2)
    let hour = ("0" + date.getHours()).slice(-2)
    let minute = ("0" + date.getMinutes()).slice(-2)
    let second = ("0" + date.getSeconds()).slice(-2)
    let thatDate = date.getFullYear() + "-" + month + "-" + sdate + " " + hour + ":" + minute + ":" + second;
    // 返回
    return thatDate;
}