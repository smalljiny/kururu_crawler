db = db.getSiblingDB("admin"); // "admin" 데이터베이스 사용

db.createUser({
  user: "mario", // 일반 사용자 이름
  pwd: "1qazxsw2", // 비밀번호
  roles: [
    { role: "readWrite", db: "kururu" }, // 특정 데이터베이스에서 읽기/쓰기 권한 부여
  ],
});
