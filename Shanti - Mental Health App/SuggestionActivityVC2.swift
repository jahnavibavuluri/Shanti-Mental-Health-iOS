//
//  ThoughtActivityVC2.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/27/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

class ThoughtActivityVC2: UIViewController {

    
    @IBOutlet weak var mainView: UIView!
    
    
    @IBOutlet weak var thought_1: UITextView!
    @IBOutlet weak var thought_2: UITextView!
    @IBOutlet weak var thought_3: UITextView!
    @IBOutlet weak var thought_4: UITextView!
    @IBOutlet weak var thought_5: UITextView!
    
    
    @IBOutlet weak var input1: UITextField!
    @IBOutlet weak var input2: UITextField!
    @IBOutlet weak var input3: UITextField!
    @IBOutlet weak var input4: UITextField!
    @IBOutlet weak var input5: UITextField!
    
    struct Thoughts:Codable {
        var thought1:String
        var thought2:String
        var thought3:String
        var thought4:String
        var thought5:String
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = view.bounds
        gradientLayer.colors = [#colorLiteral(red: 0.9686274529, green: 0.78039217, blue: 0.3450980484, alpha: 1).cgColor, #colorLiteral(red: 0.8549019694, green: 0.250980407, blue: 0.4784313738, alpha: 1).cgColor]
        gradientLayer.shouldRasterize = true
        mainView.layer.addSublayer(gradientLayer)
        
        var shouldAutorotate: Bool {
            return false
        }
        
        
        let url = URL(string: "http://127.0.0.1:5000/getrmchange")
               
        let task = URLSession.shared.dataTask(with: url!) {(data, response, error) in
        let jsonString = String(data: data!, encoding: .utf8)!
        print(jsonString)
                
        if let jsonData = jsonString.data(using: .utf8) {
            let decoder = JSONDecoder()
                    
                do {
                    let thoughts = try decoder.decode(Thoughts.self, from: jsonData)
                    let t1 = thoughts.thought1
                    let t2 = thoughts.thought2
                    let t3 = thoughts.thought3
                    let t4 = thoughts.thought4
                    let t5 = thoughts.thought5
                    OperationQueue.main.addOperation {
                        self.thought_1.text = t1
                        self.thought_2.text = t2
                        self.thought_3.text = t3
                        self.thought_4.text = t4
                        self.thought_5.text = t5
                    }
                } catch {
                    print(error)
                }
                
            } else {
                print(error!)
            }
        }
        
        task.resume()
        

        // Do any additional setup after loading the view.
    }
    
    @IBAction func doneBtn(_ sender: Any) {
         let Url = String(format: "http://127.0.0.1:5000/whatwouldichange")
        guard let serviceUrl = URL(string: Url) else { return }
        
        
        if (input1.text?.isEmpty == true || input2.text?.isEmpty == true || input3.text?.isEmpty == true || input4.text?.isEmpty == true || input5.text?.isEmpty == true) {
            OperationQueue.main.addOperation {
                let alert = UIAlertController(title: "Please Fill Out All Fields", message: "You must enter at least 5 thoughts!", preferredStyle: .alert)
                alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                self.present(alert, animated: true)
            }
            
        } else {
            let parameterDictionary = [
                "sug1":input1.text!,
                "sug2":input2.text!,
                "sug3":input3.text!,
                "sug4":input4.text!,
                "sug5":input5.text!,
            ]
            var request = URLRequest(url: serviceUrl)
            request.httpMethod = "POST"
            request.setValue("Application/json", forHTTPHeaderField: "Content-Type")
            guard let httpBody = try? JSONSerialization.data(withJSONObject: parameterDictionary, options: []) else { return }
                    request.httpBody = httpBody
            

                    let session = URLSession.shared
                    session.dataTask(with: request) { (data, response, error) in
                    if let response = response {
                        print(response)
                    }
                    if let data = data {
                        let json = String(data: data, encoding: .utf8)!
                        print(json)
                        
                    }
                           
                    }.resume()
            
        }
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
