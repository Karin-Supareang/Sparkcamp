require('dotenv').config();
const fs = require('fs');
const pdf = require('pdf-parse');
const { JamAI } = require('jamaibase');


const { insert_generated_questions } = require('./repositories/quizRepository'); 

const jamai = new JamAI({
    apiKey: process.env.JAMAI_API_KEY,
    projectId: process.env.JAMAI_PROJECT_ID
});

async function extractTextFromPDF(pdfPath) {
    const dataBuffer = fs.readFileSync(pdfPath);
    const data = await pdf(dataBuffer);
    return data.text;
}

async function generateQuizWithJamAI(contextText) {
    const prompt = `คุณคือผู้เชี่ยวชาญด้านการสอบ จงสร้างข้อสอบปรนัยจำนวน 5 ข้อจากเนื้อหาต่อไปนี้
    
    เนื้อหา:
    ${contextText}

    กรุณาส่งคืนผลลัพธ์เป็น JSON Object ในรูปแบบดังนี้เท่านั้น:
    {
        "quiz_code": "QZ-101",
        "questions": [
            {
                "question_number": 1,
                "question_text": "คำถามข้อที่ 1 คืออะไร?",
                "options_json": ["ตัวเลือก A", "ตัวเลือก B", "ตัวเลือก C", "ตัวเลือก D"],
                "correct_answer": "ตัวเลือก A",
                "topic_tag": "ชื่อหัวข้อเรื่อง"
            }
        ]
    }`;

    
    const response = await jamai.chat.completions.create({
        model: "meta/llama-3.1-8b-instruct", 
        messages: [
            { role: "system", content: "You are a helpful assistant that strictly outputs JSON format." },
            { role: "user", content: prompt }
        ],
        
        response_format: { type: "json_object" }
    });

    const outputContent = response.choices[0].message.content;
    return JSON.parse(outputContent);
}

async function main() {
    try {
        console.log("1. กำลังอ่านไฟล์ PDF...");
        const pdfText = await extractTextFromPDF("./document.pdf");

        console.log("2. กำลังส่งข้อมูลให้ JamAI ประมวลผล...");
        const quizData = await generateQuizWithJamAI(pdfText);

        console.log("3. ได้รับชุดข้อมูลคำถาม (Quiz Object) สำเร็จ:\n");
        console.log(JSON.stringify(quizData, null, 2));

        console.log("4. กำลังส่งข้อมูลไปยัง Repository เพื่อบันทึกลง Database...");
        
        
        const lectureId = 1; 

        
        const result = await insert_generated_questions({
            quiz_code: quizData.quiz_code,
            lecture_id: lectureId,
            questions: quizData.questions
        });

        console.log("✨ บันทึกข้อมูลควิซและคำถามลง Database สำเร็จเรียบร้อย!", result);

    } catch (error) {
        console.error("เกิดข้อผิดพลาดในการประมวลผล:", error);
    }
}

main();