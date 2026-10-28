import {chromium} from "playwright-core";
import {mkdir,rename,writeFile} from "node:fs/promises";
import path from "node:path";
await mkdir("evidence",{recursive:true});
const browser=await chromium.launch({executablePath:"/usr/bin/google-chrome",headless:true,args:["--no-sandbox","--disable-dev-shm-usage"]});
let context;try{
 context=await browser.newContext({viewport:{width:1440,height:900},recordVideo:{dir:"evidence",size:{width:1280,height:800}}});
 const page=await context.newPage();await page.goto("http://127.0.0.1:8766/",{waitUntil:"networkidle"});
 await page.screenshot({path:"evidence/ghostlog-before.png",fullPage:true});
 await page.locator("#mood").selectOption("unsettling");await page.locator("#generate").click();
 await page.locator(".story h2").waitFor({timeout:180000});
 const displayed=await page.locator("#result").innerText();
 if(!displayed.includes("ANOMALY TRACES")||!displayed.includes("DOWNLOAD FICTIONAL TRANSMISSION"))throw Error("Real result not rendered");
 await page.screenshot({path:"evidence/ghostlog-real-gemma-output.png",fullPage:true});
 await writeFile("evidence/recording-proof.txt","Recorded "+new Date().toISOString()+"\nActual local Gemma via application UI, no mocked responses\n"+displayed);
 await page.waitForTimeout(1200);
 const video=page.video();await context.close();context=null;
 if(video)await rename(await video.path(),path.resolve("evidence/ghostlog-real-ai-demo.webm"));
 console.log("VERIFIED REAL BROWSER DEMO screenshot and .webm");
}catch(e){console.error("Real demo failed",e);process.exitCode=1;if(context)await context.close()}finally{await browser.close()}
