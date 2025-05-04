<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learn More - QuikSend</title>
    <style>
        :root {
            --primary-color: #007BFF; /* Replace with QuikSend's primary color */
            --secondary-color: #f8f9fa; /* Replace with QuikSend's secondary color */
            --neutral-color: #343a40; /* Replace with QuikSend's neutral tones */
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            color: var(--neutral-color);
            background-color: var(--secondary-color);
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: var(--primary-color);
            color: white;
        }

        header .logo {
            font-size: 1.5rem;
            font-weight: bold;
        }

        nav {
            display: flex;
            gap: 1rem;
        }

        nav a {
            color: white;
            text-decoration: none;
            font-size: 1rem;
        }

        nav a:hover {
            text-decoration: underline;
        }

        .hero {
            text-align: center;
            padding: 4rem 2rem;
            background-color: white;
            color: var(--neutral-color);
        }

        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }

        .hero p {
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }

        .hero button {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
            color: white;
            background-color: var(--primary-color);
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .hero button:hover {
            background-color: darkblue;
        }

        .features, .how-it-works, .testimonials, .faq {
            padding: 2rem;
            text-align: center;
        }

        .features h2, .how-it-works h2, .testimonials h2, .faq h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .features .feature {
            display: inline-block;
            width: 25%;
            padding: 1rem;
        }

        footer {
            text-align: center;
            padding: 1rem;
            background-color: var(--neutral-color);
            color: white;
        }

        @media (max-width: 768px) {
            .features .feature {
                width: 100%;
            }

            nav {
                flex-direction: column;
                gap: 0.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="logo">QuikSend</div>
        <nav>
            <a href="#">Home</a>
            <a href="#">Features</a>
            <a href="#">Pricing</a>
            <a href="#">Support</a>
        </nav>
    </header>

    <section class="hero">
        <h1>Take Your Email Marketing to the Next Level</h1>
        <p>Learn how QuikSend can help you automate, schedule, and analyze email campaigns with ease.</p>
        <button>Discover More</button>
    </section>

    <section class="features">
        <h2>Features</h2>
        <div class="feature">
            <h3>Automation</h3>
            <p>Simplify your email workflows.</p>
        </div>
        <div class="feature">
            <h3>Analytics</h3>
            <p>Gain insights with detailed reporting.</p>
        </div>
        <div class="feature">
            <h3>Template Designs</h3>
            <p>Create professional emails effortlessly.</p>
        </div>
        <div class="feature">
            <h3>Audience Segmentation</h3>
            <p>Target the right audience.</p>
        </div>
    </section>

    <footer>
        <p>&copy; 2025 QuikSend. All rights reserved.</p>
    </footer>
</body>
</html>
