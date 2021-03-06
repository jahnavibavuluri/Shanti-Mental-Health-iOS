//
//  ViewController.swift
//  Shanti - Mental Health App
//
//  Created by Jahnavi Bavuluri  on 7/8/20.
//  Copyright © 2020 Jahnavi Bavuluri . All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    
    @IBOutlet weak var mainView: UIView!
    @IBOutlet weak var usernameField: UITextField!
    @IBOutlet weak var passwordField: UITextField!

    override var preferredStatusBarStyle: UIStatusBarStyle {
        return .darkContent
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        usernameField.delegate = self
        passwordField.delegate = self
        
        let gradientLayer = CAGradientLayer()
        gradientLayer.frame = view.bounds
        gradientLayer.colors = [#colorLiteral(red: 0.9686274529, green: 0.78039217, blue: 0.3450980484, alpha: 1).cgColor, #colorLiteral(red: 0.8549019694, green: 0.250980407, blue: 0.4784313738, alpha: 1).cgColor]
        gradientLayer.shouldRasterize = true
        mainView.layer.addSublayer(gradientLayer)
        
        var shouldAutorotate: Bool {
            return false
        }


    }
    
    
    @IBAction func loginUser(_ sender: Any) {
        let Url = String(format: "http://127.0.0.1:5000/login")
        guard let serviceUrl = URL(string: Url) else { return }
        let parameterDictionary = ["username" : usernameField.text!, "password" : passwordField.text!]
        var request = URLRequest(url: serviceUrl)
        request.httpMethod = "POST"
        request.setValue("Application/json", forHTTPHeaderField: "Content-Type")
        guard let httpBody = try? JSONSerialization.data(withJSONObject: parameterDictionary, options: []) else {
                return
            }
        request.httpBody = httpBody

        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let response = response {
                print(response)
            }
            if let data = data {
                let json = String(data: data, encoding: .utf8)!
                print(json)
                if (json=="invalid password") {
                    OperationQueue.main.addOperation {
                        let alert = UIAlertController(title: "Invalid Password", message: "Your password is not valid!", preferredStyle: .alert)
                        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                        self.present(alert, animated: true)
                    }
                } else if (json=="no user") {
                   OperationQueue.main.addOperation {
                        let alert = UIAlertController(title: "No User Found", message: "Either you have entered in the wrong username or we do not have an account under that name.", preferredStyle: .alert)
                        alert.addAction(UIAlertAction(title: "OK", style: .default, handler: nil))
                        self.present(alert, animated: true)
                    }
                } else {
                    OperationQueue.main.addOperation {
                        self.performSegue(withIdentifier: "welcomeSegue", sender: self)
                    }
                }
            }
            }.resume()
        }
    
    
    @IBAction func signupButton(_ sender: Any) {
        performSegue(withIdentifier: "signinSegue", sender: self)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "welcomeSegue" {
            var vc = segue.destination as! UITabBarController
        }
        
        if segue.identifier == "signinSegue" {
            var vc = segue.destination as! SignupViewController
        }
       
    }
    
    }


extension ViewController : UITextFieldDelegate {
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        textField.resignFirstResponder()
        return true
    }
}
