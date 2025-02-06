import React, { useState } from "react";
import "./RegistrationForm.css";
import axios from 'axios';

const RegistrationForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [address_line1, setAddressLine1] = useState('');
  const [address_line2, setAddressLine2] = useState('');
  const [city, setCity] = useState('');
  const [postcode, setPostCode] = useState('');
  const [attending_date, setAttendingDate] = useState('');
  const [numPeople, setNumPeople] = useState(0);
  const [ages, setAges] = useState([]);
  const [transport, setTransport] = useState('');
  const [carPool, setCarPool] = useState(false);
  const [carPoolSeats, setCarPoolSeats] = useState(0);
  const [accommodation, setAccommodation] = useState("");
  const [homeSpace, setHomeSpace] = useState(false);
  const [homeSpaceCount, setHomeSpaceCount] = useState(0);
  const [totalFees, setTotalFees] = useState(0);
  const [paymentConfirmed, setPaymentConfirmed] = useState(false);
  const [gdprConsent, setGdprConsent] = useState(false);


  const handleNumPeopleChange = (e) => {
    const count = parseInt(e.target.value, 10) || 0;
    setNumPeople(count);
    setAges(new Array(count).fill(""));
  };

  const handleAgeChange = (index, value) => {
    const newAges = [...ages];
    newAges[index] = value;
    setAges(newAges);

    let fees = 0;
    newAges.forEach((age) => {
      if (age === "15+") fees += 10;
      if (age === "5-15") fees += 5;
    });

    setTotalFees(fees);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!paymentConfirmed || !gdprConsent) {
      alert("You must confirm payment and agree to GDPR policy.");
      return;
    }
    
    const formData = {
      name,
      email,
      phone,
      address_line1,
      address_line2,
      city,
      postcode,
      numPeople,
      ages,
      attending_date,
      transport,
      carPool,
      carPoolSeats,
      accommodation, 
      homeSpace,
      homeSpaceCount,
      totalFees,
      paymentConfirmed,
    }

    try {
      const response = await axios.post("http://localhost:8000/register", formData);
      alert("Registration successful! ID: " + response.data.RegistrationId);
      console.log(response.data.RegistrationId)
    } catch (error) {
      alert("Registration failed: " + error.response.data.detail);
    }
  };

  return (
    <div className="form-container">
      <h2>Registration Form</h2>

      <form onSubmit={handleSubmit}>
        {/* Name & Email */}
        <div className="form-group">
          <div className="input-box">
            <label>Name</label>
            <input type="text" required value={name} onChange={(e)=>setName(e.target.value)} />
          </div>
          
        </div>

        {/* Phone */}
        <div className="form-group">
          <div className="input-box">
            <label>Phone</label>
            <input type="tel" required value={phone} onChange={(e)=>setPhone(e.target.value)} />            
          </div>
        </div>
        <div className="form-group">  
          <div className="input-box">
            <label>Email</label>
            <input type="email" required value={email} onChange={(e)=>setEmail(e.target.value)} />            
          </div>
        </div>
        {/* Address */}
        <div className="form-group">
          <div className="input-box">
            <label>Address Line 1</label>
            <input type="text" required value={address_line1} onChange={(e)=>setAddressLine1(e.target.value)} />
          </div>
        </div>
        <div className="form-group">  
          <div className="input-box">
            <label>Address Line 2</label>
            <input type="text" value={address_line2} onChange={(e)=>setAddressLine2(e.target.value)} />
          </div>
        </div>

        <div className="form-group">
          <div className="input-box">
            <label>City</label>
            <input type="text" required value={city} onChange={(e)=>setCity(e.target.value)} />
          </div>
        </div>
        <div className="form-group">  
          <div className="input-box">
            <label>Postcode</label>
            <input type="text" required value={postcode} onChange={(e)=>setPostCode(e.target.value)} />
          </div>
        </div>

        {/* Number of People */}
        <div className="form-group">
          <div className="input-box">
            <label>Number of People</label>
            <input
              type="number"
              min={1}
              value={numPeople}
              onChange={handleNumPeopleChange}
              required
            />
          </div>
        </div>

        {/* Age Selection */}
        {numPeople > 0 &&
          ages.map((age, index) => (
            <div key={index} className="form-group">
              <div className="input-box">
                <label>Age of Person {index + 1}</label>
                <select value={age} onChange={(e) => handleAgeChange(index, e.target.value)} required>
                  <option value="">Select Age</option>
                  <option value="under-5">Under 5 (Free)</option>
                  <option value="5-15">5-15 (£5)</option>
                  <option value="15+">15+ (£10)</option>
                </select>  
              </div>            
            </div>
          ))}

        {/* Date Attending */}
        <div className="form-group">
          <div className="input-box">
            <label>Select Date Attending</label>
            <select required value={attending_date} onChange={(e)=>setAttendingDate(e.target.value)} >
              <option value="" hidden>Select Date Attending</option>
              <option value="12th April">12th April 2025</option>
              <option value="13th April">13th April 2025</option>
            </select>
          </div>
        </div>

        {/* Medium of Transport */}
        <div className="form-group">
          <div className="input-box">
            <label>Select Transport</label>
            <select
              value={transport}
              onChange={(e) => setTransport(e.target.value)}
              required
            >
              <option value="" hidden>Select Transport</option>
              <option value="car">Car</option>
              <option value="public">Public Transport</option>
            </select>
          </div>
        </div>

        {/* Car Pool Options */}
        {transport === "car" && (
          <>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={carPool}
                  onChange={() => setCarPool(!carPool)}
                />
                Do you have any extra space for carpooling?
              </label>
            </div>
            {carPool && (
              <div className="form-group">
                <div className="input-box">
                  <label>How many seats available?</label>
                  <input
                    type="number"
                    min="1"
                    max="5"
                    value={carPoolSeats}
                    onChange={(e) => setCarPoolSeats(e.target.value)}
                  />
                </div>
              </div>
            )}
          </>
        )}

        {/* Accommodation */}
        <div className="form-group">
          <div className="input-box">
            <label>Select Accommodation</label>
            <select
              value={accommodation}
              onChange={(e) => setAccommodation(e.target.value)}
              required
            >
              <option value="" hidden>Select Accommodation *</option>
              <option value="friends">Friend's House</option>
              <option value="hotel">Hotel</option>
              <option value="own">Own Home</option>
            </select>
          </div>
        </div>

        {/* Home Accommodation Options */}
        {accommodation === "own" && (
          <>
            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={homeSpace}
                  onChange={() => setHomeSpace(!homeSpace)}
                />
                Do you have space for accommodation?
              </label>
              
            </div>
            {homeSpace && (
              <div className="form-group">
                <div className="input-box">
                  <label>How many people?</label>
                  <input
                    type="number"
                    min="1"
                    max="5"
                    value={homeSpaceCount}
                    onChange={(e) => setHomeSpaceCount(e.target.value)}
                  />                  
                </div>
              </div>
            )}
          </>
        )}
        {/* Total Cost Calculation */}
        <div className="form-group">
          <p><strong>Total Fees: £{totalFees}</strong></p>
        </div>

        {/* Payment Confirmation */}
        <div className="form-group">
          <label>
            <input type="checkbox" checked={paymentConfirmed} onChange={(e)=>setPaymentConfirmed(e.target.checked)} /> I confirm the payment is done.
          </label>
        </div>

        <div className="form-group gdpr-consent">
          <label>
            <input type="checkbox" checked={gdprConsent} onChange={(e)=>{setGdprConsent(e.target.checked)}} /> 
            I agree to the collection and processing of my personal data in accordance with the <a href="/privacy-policy" target="_blank">Privacy Policy</a>.
          </label>
        </div>

        {/* Submit Button */}
        <button type="submit">Submit</button>
      </form>

      {/* Withdrawal Policy */}
      <div className="form-group">
        <p style={{ fontSize: "14px", color: "#666" }}>
          *You can withdraw your registration before the deadline and receive a full refund.
        </p>
      </div>
    </div>
  );
};

export default RegistrationForm;
